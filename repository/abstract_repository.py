from database.connection import Database
from abc import abstractmethod
from repository.abstract_connection_repository import AbstractConnectionRepository

# Deze abstracte class definieert welke methods minimaal aanwezig dienen te zijn in een repository
# De methods zijn van toepassing op alle repositories die verbinding leggen met de specifieke database tabel
# De methods omvatten volledige CRUD interactie met de specifieke database tabel
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