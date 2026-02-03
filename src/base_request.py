from abc import ABC, abstractmethod
from typing import Any


class BaseRequest(ABC):
    """Абстрактный класс запросов к внешним ресурсам"""

    @abstractmethod
    def get_response(self) -> Any:
        """Абстрактный метод get-запросов"""

        pass
