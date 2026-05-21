from fastapi import APIRouter, Depends
from app.core.admission_control import should_accept_request, within_token_budget
from app.core.api_key_auth import get_api_key
from app.core.request_scheduler import enqueue_request
from app.core.retry import MAX_RETRIES, exponential_backoff
from app.models.api_key import APIKey
import asyncio
from app.services.rate_limiter import check_rate_limit
from fastapi import HTTPException

from sse_starlette.sse import EventSourceResponse
import asyncio
import time
from app.services.log_service import create_request_log, queue_request_log
from app.db.session import SessionLocal

from app.providers.provider_factory import ProviderFactory
from app.schemas.completion import CompletionRequest
from app.routing.router import ProviderRouter
from app.registry.provider_registry import ProviderRegistry

import uuid
from app.core.logger import logger

from app.core.metrics import ESTIMATED_COST, GLOBAL_ACTIVE_REQUESTS, REJECTED_REQUESTS, REQUEST_COUNT, REQUEST_LATENCY, FALLBACK_COUNT, ACTIVE_STREAMS, RETRY_COUNT, STREAM_COUNT, TOKEN_USAGE
from app.core.metrics import STREAM_FAILURES, STREAM_DURATION, TOKENS_STREAMED
from app.core.tracing import tracer
from opentelemetry import trace

from fastapi.responses import StreamingResponse
from starlette.requests import Request

router = APIRouter(prefix="/v1", tags=["gateway"])





@router.post("/completions")
async def completions(
    request: CompletionRequest,
    request_obj: Request,
    api_key: APIKey = Depends(get_api_key)
):

    request_start = time.time()

    request_id = str(uuid.uuid4())

    # ---------------------------------------------------
    # Rate Limiting
    # ---------------------------------------------------

    allowed, limit, current = check_rate_limit(
        api_key.id,
        api_key.tier
    )

    if not allowed:

        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded❗"
        )

    router_instance = ProviderRouter()

    # ---------------------------------------------------
    # Provider Selection
    # ---------------------------------------------------

    # Manual provider selection
    if request.provider:

        provider_name = request.provider

    # Automatic orchestration routing
    else:

        provider_name = router_instance.get_provider(
            strategy_name=request.strategy,
            model_name=request.model,
            user_tier = api_key.tier
        )

    # ---------------------------------------------------
    # Fallback Logic
    # ---------------------------------------------------

    # Strict provider mode
    if request.strict_provider:

        fallback_chain = [provider_name]

    # Flexible orchestration mode
    else:

        fallback_chain = (
            router_instance.get_fallback_chain(
                provider_name
            )
        )

    last_error = None
    response = None

    accepted = should_accept_request(provider_name,api_key.tier, api_key.user_id)
    if not accepted:
        REJECTED_REQUESTS.labels(reason="overload").inc()
        # raise HTTPException(

        #     status_code=503,

        #     detail=(
        #         "Gateway overloaded. "
        #         "Please retry later."
        #     )
        # )
        payload = {"prompt": request.prompt,
            "provider": provider_name,
            "model": request.model,
            "user_id": api_key.user_id,
            "queued_at": time.time()
        }
        enqueue_request(payload,api_key.tier)

        return {
            "status": "queued",
            "message": (
                "Request queued due to "
                "temporary overload"
            )
        }

    estimated_tokens = max(
        len(request.prompt.split()) * 2,
        50
    )

    allowed = within_token_budget(
        api_key.user_id,
        api_key.tier,
        estimated_tokens
    )

    if not allowed:

        raise HTTPException(

            status_code=403,

            detail=(
                "Token budget exceeded"
            )
        )


    # ---------------------------------------------------
    # Streaming Path
    # ---------------------------------------------------
    
    if request.stream:

        # NOTE:
        # Streaming currently does NOT support
        # fallback orchestration.

        provider = (
            ProviderFactory.get_provider(
                provider_name
            )
        )
        

        async def stream_generator():

            with tracer.start_as_current_span(
                "streaming_response"
            ):

                current_span = (
                    trace.get_current_span()
                )

                current_span.set_attribute(
                    "provider",
                    provider_name
                )

                current_span.set_attribute(
                    "streaming",
                    True
                )

                current_span.set_attribute(
                    "model",
                    request.model or "none"
                )

                stream_start = time.time()

                ACTIVE_STREAMS.inc()

                STREAM_COUNT.inc()

                token_count = 0
                ProviderRegistry.increment_active_requests(provider_name)
                ProviderRegistry.increment_tenant_requests(api_key.user_id)
                try:
                    GLOBAL_ACTIVE_REQUESTS.inc()

                    async for chunk in (
                        provider.stream_response(
                            request.prompt
                        )
                    ):

                        if await request_obj.is_disconnected():

                            logger.warning(

                                "client_disconnected",

                                extra={

                                    "extra_data": {

                                        "request_id": request_id,

                                        "provider": provider_name
                                    }
                                }
                            )

                            break
                        

                        token_count += 1

                        TOKENS_STREAMED.inc()

                        yield chunk

                except Exception as e:

                    STREAM_FAILURES.inc()

                    logger.error(

                        "stream_failed",

                        extra={

                            "extra_data": {

                                "request_id": request_id,

                                "provider": provider_name,

                                "error": str(e)
                            }
                        }
                    )

                    raise

                finally:

                    ACTIVE_STREAMS.dec()
                    GLOBAL_ACTIVE_REQUESTS.dec()
                    ProviderRegistry.decrement_active_requests(
                        provider_name
                    )
                    ProviderRegistry.decrement_tenant_requests(
                        api_key.user_id
                    )

                    STREAM_DURATION.observe(
                        time.time() - stream_start
                    )

                    logger.info(

                        "stream_completed",

                        extra={

                            "extra_data": {

                                "request_id": request_id,

                                "provider": provider_name,

                                "tokens_streamed": token_count,

                                "stream_duration": (
                                    time.time()
                                    - stream_start
                                )
                            }
                        }
                    )
                    queue_request_log(
                        user_id=api_key.user_id,
                        api_key_id=api_key.id,
                        endpoint="/v1/completions",
                        method="POST",
                        status_code=200,
                        latency_ms=int(
                            (time.time() - stream_start) * 1000
                        ),
                        tokens_used=token_count
                    )

        return StreamingResponse(

            stream_generator(),

            media_type="text/plain"
        )

    # ---------------------------------------------------
    # Non-Streaming Provider Execution
    # ---------------------------------------------------

    with tracer.start_as_current_span(
        "provider_execution"
    ):

        GLOBAL_ACTIVE_REQUESTS.inc()
        try:
            ProviderRegistry.increment_tenant_requests(api_key.user_id)
            for candidate_provider in fallback_chain:

                current_span = (
                    trace.get_current_span()
                )

                current_span.set_attribute(
                    "provider",
                    candidate_provider
                )

                current_span.set_attribute(
                    "model",
                    request.model or "none"
                )

                try:

                    provider = (
                        ProviderFactory.get_provider(
                            candidate_provider
                        )
                    )

                    # response = (
                    #     await provider.generate_response(
                    #         prompt=request.prompt
                    #     )
                    # )


                    for attempt in range(MAX_RETRIES):
                        ProviderRegistry.increment_active_requests(
                            candidate_provider
                        )
                        

                        try:
                            response = (await provider.generate_response(prompt=request.prompt))

                            break

                        except Exception as retry_error:

                            RETRY_COUNT.labels(provider=candidate_provider).inc()
                            current_span.set_attribute("retry_attempt",attempt)
                            logger.warning(
                                "provider_retry",
                                extra={
                                    "extra_data": {
                                        "provider": candidate_provider,
                                        "attempt": attempt + 1
                                    }
                                }
                            )

                            if attempt == MAX_RETRIES - 1:
                                raise retry_error
                            await exponential_backoff(attempt)

                        finally:
                            ProviderRegistry.decrement_active_requests(
                                candidate_provider
                            )
                            


                    # tokens_used = len(
                    #     str(response).split()
                    # )

                    # Reset provider failures after success
                    ProviderRegistry.reset_failures(
                        candidate_provider
                    )

                    # Fallback metric
                    if candidate_provider != fallback_chain[0]:

                        FALLBACK_COUNT.inc()

                    provider_name = candidate_provider

                    break

                except Exception as e:

                    # Track provider failures
                    ProviderRegistry.mark_failure(
                        candidate_provider
                    )

                    logger.error(

                        "provider_request_failed",

                        extra={

                            "extra_data": {

                                "request_id": request_id,

                                "provider": candidate_provider,

                                "error": str(e)
                        }
                    }
                    )

                    last_error = str(e)

            else:
                raise HTTPException(
                    status_code=503,
                    detail=(
                        f"All providers failed: "
                        f"{last_error}"
                    )
                )

        finally:
            GLOBAL_ACTIVE_REQUESTS.dec()
            ProviderRegistry.decrement_tenant_requests(
                                api_key.user_id
                            )

    # ---------------------------------------------------
    # Metrics / Logging
    # ---------------------------------------------------

    latency_ms = int(
        (time.time() - request_start) * 1000
    )
    tokens_used = len(
        str(response).split()
    )

    ProviderRegistry.increment_token_usage(
        api_key.user_id,
        tokens_used
    )
    TOKEN_USAGE.labels(
        tier=api_key.tier
    ).inc(tokens_used)

    cost = (
        ProviderRegistry.estimate_request_cost(

            provider_name,

            tokens_used
        )
    )

    ESTIMATED_COST.labels(
        provider=provider_name
    ).inc(cost)

    queue_request_log(
        user_id=api_key.user_id,
        api_key_id=api_key.id,
        endpoint="/v1/completions",
        method="POST",
        status_code=200,
        latency_ms=latency_ms,
        tokens_used=tokens_used
    )

    logger.info(

        "completion_request_processed",

        extra={
            "extra_data": {

                "request_id": request_id,

                "provider_used": provider_name,

                "model_requested": request.model,

                "latency_ms": latency_ms,

                "fallback_used": (
                    provider_name
                    != request.provider
                    if request.provider
                    else False
                ),

                "user_id": api_key.user_id,

                "tier": api_key.tier
            }
        }
    )
    ProviderRegistry.record_success(

        provider_name=candidate_provider,

        latency_ms=latency_ms
    )

    REQUEST_LATENCY.labels(
        provider=provider_name
    ).observe(

        time.time() - request_start
    )

    REQUEST_COUNT.labels(

        provider=provider_name,

        status="success"

    ).inc()

    

    # ---------------------------------------------------
    # Response
    # ---------------------------------------------------

    return {

        "provider_used": provider_name,

        "model_requested": request.model,

        "response": response,

        "tier": api_key.tier,

        "usage": f"{current}/{limit}"
    }


async def fake_token_stream():

    tokens = [
        "Hello",
        "Hello how",
        "Hello how are",
        "Hello how are you",
    ]

    for token in tokens:
        yield {
            "event": "message",
            "data": token
        }

        await asyncio.sleep(1)


@router.get("/stream/completions")
async def stream_completion(api_key:APIKey = Depends(get_api_key)):
    return EventSourceResponse(fake_token_stream())


