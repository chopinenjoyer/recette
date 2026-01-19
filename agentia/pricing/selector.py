from agentia.pricing.intermarche import IntermarcheProvider
from agentia.pricing.estimated import EstimatedProvider

def get_price_provider(store: str):
    if store.lower() == "intermarché":
        return IntermarcheProvider()
    return EstimatedProvider()
