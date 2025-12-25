from agentia.pricing.base import PriceProvider

class EstimatedProvider(PriceProvider):
    def get_prices(self, ingredients):
        results = []
        for ingredient in ingredients:
            results.append({
                "ingredient": ingredient,
                "store": "Estimation",
                "price": "estimation",
                "unit": "variable"
            })
        return results
