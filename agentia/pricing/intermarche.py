import requests
from os import getenv
from typing import List, Dict
from agentia.pricing.base import PriceProvider

BASE_URL = "https://api-partners.intermarche.com/produits/v1"

class IntermarcheProvider(PriceProvider):

    def __init__(self):
        self.api_key = getenv("INTERMARCHE_API_KEY")
        if not self.api_key:
            raise RuntimeError("INTERMARCHE_API_KEY manquant dans le fichier .env")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def get_pdv(self, lat: float, lon: float) -> str:
        params = {
            "nw_lat": lat + 0.1,
            "nw_lon": lon - 0.1,
            "se_lat": lat - 0.1,
            "se_lon": lon + 0.1,
            "min": 1,
        }

        r = requests.get(
            f"{BASE_URL}/pdvs/zone",
            headers=self.headers,
            params=params,
            timeout=10,
        )
        r.raise_for_status()

        return r.json()["pdvs"][0]["id"]

    def search_product(self, pdv_id: str, keyword: str) -> Dict | None:
        payload = {
            "keyword": keyword,
            "page": 0,
            "size": 1
        }

        r = requests.post(
            f"{BASE_URL}/pdvs/{pdv_id}/produits/search",
            headers=self.headers,
            json=payload,
            timeout=10,
        )
        r.raise_for_status()

        products = r.json().get("products", [])
        return products[0] if products else None

    def get_product_detail(self, pdv_id: str, product_id: str) -> Dict:
        r = requests.get(
            f"{BASE_URL}/pdvs/{pdv_id}/produits/{product_id}",
            headers=self.headers,
            timeout=10,
        )
        r.raise_for_status()
        return r.json()

    def get_prices(self, ingredients: List[str]) -> List[Dict]:
        pdv_id = self.get_pdv(lat=48.8566, lon=2.3522)  
        results = []

        for ingredient in ingredients:
            product = self.search_product(pdv_id, ingredient)
            if not product:
                results.append({
                    "ingredient": ingredient,
                    "store": "Intermarché",
                    "error": "Produit non trouvé"
                })
                continue

            detail = self.get_product_detail(pdv_id, product["id"])

            price = detail.get("prix", {})
            nutrition = detail.get("nutrition", {})

            results.append({
                "ingredient": ingredient,
                "store": "Intermarché",
                "product_name": detail.get("libelle"),
                "price": price.get("prixTTC"),
                "unit": price.get("unite"),
                "nutriscore": detail.get("nutriScore"),
                "nutrition": nutrition
            })

        return results
