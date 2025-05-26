from database.connection import Database
from abc import abstractmethod
from repository.abstract_connection_repository import AbstractConnectionRepository

# Een Hydrated Repostiory class legt verbinding met verschillende database tabellen tegenlijk
# Relationele data wordt opgehaald tijdens een query door middel van JOIN statements
# De methods omvatten enkel de READ interacties met de specifieke database tabel
class AbstractHydratedRepository(AbstractConnectionRepository):

    _DIVIDER = '__'

    def __init__(self, db: Database):
        super().__init__(db)

    @abstractmethod
    def get_all(self) -> list:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> object | None:
        pass