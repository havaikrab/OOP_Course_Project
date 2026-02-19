from abc import ABC, abstractmethod
from typing import Any


class BaseManager(ABC):
    """Абстрактный класс работы с файлами, обязующий классы-наследники описывать
    методы добавления, удаления, извлечения информации из соответствующего файла"""

    @abstractmethod
    def write_data(self, data: Any) -> None:
        """Абстрактный метод записи информации в файл"""

        pass

    @abstractmethod
    def read_data(self) -> Any:
        """Абстрактный метод получения информации из файла"""

        pass

    @abstractmethod
    def clear_data(self) -> Any:
        """Абстрактный метод удаления всей информации из файла"""

        pass
