from repository.abstract_repository import AbstractRepository
from model.fiets_type import FietsType

# Complete CRUD interactie met de FietsType tabel
class FietsTypeRepository(AbstractRepository):
    FIETS_TYPE_TABLE = 'fiets_type'

    def get_all(self) -> list[FietsType]:
        fiets_typen_list = []

        query = 'SELECT * FROM ' + self.FIETS_TYPE_TABLE
        for query_result in self._fetch_all(query):
            fiets_typen_list.append(FietsType(query_result))

        return fiets_typen_list

    def get_by_id(self, id: int) -> FietsType | None:
        query = 'SELECT * FROM ' + self.FIETS_TYPE_TABLE + ' WHERE fiets_type_id = %s'
        query_result = self._fetch_one(query, (id,))

        if query_result is None:
            return None

        return FietsType(query_result)

    def delete_by_id(self, id: int) -> None:
        query = 'DELETE FROM ' + self.FIETS_TYPE_TABLE + ' WHERE fiets_type_id = %s'
        self._execute_and_commit_query(query, (id,))

    def insert(self, model: FietsType) -> int:
        query = 'INSERT INTO ' + self.FIETS_TYPE_TABLE + ' (beschrijving, model, electrisch, dagprijs) VALUES (%s, %s, %s, %s)'
        params = (model.beschrijving, model.model, model.electrisch, model.dagprijs)
        cursor = self._execute_and_commit_query(query, params)
        return int(cursor.lastrowid)

    def update(self, model: FietsType) -> None:
        query = 'UPDATE ' + self.FIETS_TYPE_TABLE + ' SET beschrijving = %s, model = %s, electrisch = %s, dagprijs = %s WHERE fiets_type_id = %s'
        params = (model.beschrijving, model.model, model.electrisch, model.dagprijs, model.fiets_type_id)
        self._execute_and_commit_query(query, params)