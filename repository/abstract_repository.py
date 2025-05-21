from database.connection import Database
from abc import abstractmethod
from repository.abstract_connection_repository import AbstractConnectionRepository

class AbstractRepository(AbstractConnectionRepository):
    def __init__(self, db: Database):
        super().__init__(db)

    @abstractmethod
    def get_all(self) -> list:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> object | None:
        pass

    @abstractmethod
    def delete_by_id(self, id: int) -> None:
        pass

    @abstractmethod
    def insert(self, model : object) -> int:
        pass

    @abstractmethod
    def update(self, model : object) -> None:
        pass