from repository.abstract_repository import AbstractRepository
from model.fiets import Fiets
from repository.contract_fiets_repository import ContractFietsRepository
from repository.contract_repository import ContractRepository

# Complete CRUD interactie met de Fiets tabel
class FietsRepository(AbstractRepository):
    FIETS_TABLE = 'fiets'

    def get_all(self) -> list[Fiets]:
        fietsen_list = []

        query = 'SELECT * FROM ' + self.FIETS_TABLE
        for query_result in self._fetch_all(query):
            fietsen_list.append(Fiets(query_result))

        return fietsen_list

    def get_by_id(self, id: int) -> Fiets | None:
        query = 'SELECT * FROM ' + self.FIETS_TABLE + ' WHERE fiets_id = %s'
        query_result = self._fetch_one(query, (id,))

        if query_result is None:
            return None

        return Fiets(query_result)

    def delete_by_id(self, id: int) -> None:
        query = 'DELETE FROM ' + self.FIETS_TABLE + ' WHERE fiets_id = %s'
        self._execute_and_commit_query(query, (id,))

    def insert(self, model: Fiets) -> int:
        query = 'INSERT INTO ' + self.FIETS_TABLE + ' (merk, aankoop_datum, fiets_type_id) VALUES (%s, %s, %s)'
        params = (model.merk, model.aankoop_datum, model.fiets_type_id)
        cursor = self._execute_and_commit_query(query, params)
        return int(cursor.lastrowid)

    def update(self, model: Fiets) -> None:
        query = 'UPDATE ' + self.FIETS_TABLE + ' SET merk = %s, aankoop_datum = %s, fiets_type_id = %s WHERE fiets_id = %s'
        params = (model.merk, model.aankoop_datum, model.fiets_type_id, model.fiets_id)
        self._execute_and_commit_query(query, params)