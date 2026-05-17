from fastapi import APIRouter, Depends
from app.core.api_key_auth import get_api_key
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

router = APIRouter(prefix="/v1", tags=["gateway"])

@router.post("/completions")
async def completions(
    request: CompletionRequest,
    api_key: APIKey = Depends(get_api_key)
):

    start_time = time.time()
    request_id = str(uuid.uuid4())

    # Rate limiting
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
            model_name=request.model
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

    # ---------------------------------------------------
    # Provider Execution Loop
    # ---------------------------------------------------

    for candidate_provider in fallback_chain:

        try:

            provider = (
                ProviderFactory.get_provider(
                    candidate_provider
                )
            )

            response = (
                await provider.generate_response(
                    prompt=request.prompt
                )
            )

            # Reset provider failures after success
            ProviderRegistry.reset_failures(
                candidate_provider
            )

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

    # ---------------------------------------------------
    # Metrics / Logging
    # ---------------------------------------------------

    latency_ms = int(
        (time.time() - start_time) * 1000
    )

    queue_request_log(
        user_id=api_key.user_id,
        api_key_id=api_key.id,
        endpoint="/v1/completions",
        method="POST",
        status_code=200,
        latency_ms=latency_ms,
        tokens_used=50
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


