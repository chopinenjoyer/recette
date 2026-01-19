from abc import ABC, abstractmethod
from typing import List, Dict

class PriceProvider(ABC):
    @abstractmethod
    def get_prices(self, ingredients: List[str]) -> List[Dict]:
        pass
