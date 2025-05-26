from repository.abstract_repository import AbstractRepository
from model.contract import Contract

# Complete CRUD interactie met de Contract tabel
class ContractRepository(AbstractRepository):
    CONTRACT_TABLE = 'contract'

    def get_all(self) -> list[Contract]:
        contracten_list = []

        query = 'SELECT * FROM ' + self.CONTRACT_TABLE
        for query_result in self._fetch_all(query):
            contracten_list.append(Contract(query_result))

        return contracten_list

    def get_by_id(self, id: int) -> Contract | None:
        query = 'SELECT * FROM ' + self.CONTRACT_TABLE + ' WHERE contract_id = %s'
        query_result = self._fetch_one(query, (id,))

        if query_result is None:
            return None

        return Contract(query_result)

    def delete_by_id(self, id: int) -> None:
        query = 'DELETE FROM ' + self.CONTRACT_TABLE + ' WHERE contract_id = %s'
        self._execute_and_commit_query(query, (id,))

    def insert(self, model: Contract) -> int:
        query = 'INSERT INTO ' + self.CONTRACT_TABLE + ' (klant_id, vestiging_id, start_datum, eind_datum) VALUES (%s, %s, %s, %s)'
        params = (model.klant_id, model.vestiging_id, model.start_datum, model.eind_datum)
        cursor = self._execute_and_commit_query(query, params)
        return int(cursor.lastrowid)

    def update(self, model : Contract) -> None:
        query = 'UPDATE ' + self.CONTRACT_TABLE + ' SET klant_id = %s, vestiging_id = %s, start_datum = %s, eind_datum = %s WHERE contract_id = %s'
        params = (model.klant_id, model.vestiging_id, model.start_datum, model.eind_datum, model.contract_id)
        self._execute_and_commit_query(query, params)

    # Zoek alle contracten op voor een specifieke klant
    def get_by_klant_id(self, klant_id: int) -> list[Contract]:
        contracten_list = []

        query = 'SELECT * FROM ' + self.CONTRACT_TABLE + ' WHERE klant_id = %s'

        for query_result in self._fetch_all(query, (klant_id,)):
            contracten_list.append(Contract(query_result))

        return contracten_list