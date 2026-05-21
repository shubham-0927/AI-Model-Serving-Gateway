from app.registry.provider_registry import ProviderRegistry

MAX_GLOBAL_REQUESTS = 100
MAX_PROVIDER_LOAD = 20
TENANT_LIMITS = {

    "free": 5,

    "premium": 20
}
TOKEN_BUDGETS = {

    "free": 50000,

    "premium": 2000000
}


def should_accept_request(provider_name: str,user_tier: str, user_id:int):
    total_active = 0
    for provider in (ProviderRegistry.get_all_providers()):
        total_active += (ProviderRegistry.get_active_requests(provider))

    # Premium users get priority
    if user_tier == "premium":

        global_limit = (MAX_GLOBAL_REQUESTS * 1.5)

    else:
        global_limit = (MAX_GLOBAL_REQUESTS)
    if total_active >= global_limit:
        return False
    provider_load = (ProviderRegistry.get_active_requests(provider_name))
    if provider_load >= MAX_PROVIDER_LOAD:
        return False
    

    tenant_requests = (ProviderRegistry.get_tenant_requests(user_id))
    tenant_limit = (TENANT_LIMITS[user_tier])
    if tenant_requests >= tenant_limit:
        return False
    return True

def within_token_budget(

    user_id: int,

    user_tier: str,

    estimated_tokens: int
):

    current_usage = (
        ProviderRegistry.get_token_usage(
            user_id
        )
    )

    budget = (
        TOKEN_BUDGETS[user_tier]
    )

    projected = (
        current_usage
        + estimated_tokens
    )

    return projected <= budget