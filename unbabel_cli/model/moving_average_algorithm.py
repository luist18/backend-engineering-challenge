from typing import Dict, Any
from abc import abstractmethod


class MovingAverageAlgorithm:
    @abstractmethod
    def moving_average(self, events: [Dict[str, Any]], window: int = 10) -> [Dict[str, Any]]:
        pass
