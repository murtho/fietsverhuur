from repository.abstract_repository import AbstractRepository
from model.contract_fiets import ContractFiets

class ContractFietsRepository(AbstractRepository):
    CONTRACT_FIETS_TABLE = 'contract_fiets'

    def get_all(self) -> list[ContractFiets]:
        contract_fietsen_list = []

        query = 'SELECT * FROM ' + self.CONTRACT_FIETS_TABLE
        for query_result in self._fetch_all(query):
            contract_fietsen_list.append(ContractFiets(query_result))

        return contract_fietsen_list

    def get_by_id(self, id: int) -> ContractFiets | None:
        query = 'SELECT * FROM ' + self.CONTRACT_FIETS_TABLE + ' WHERE contract_fiets_id = %s'
        query_result = self._fetch_one(query, (id,))

        if query_result is None:
            return None

        return ContractFiets(query_result)

    def delete_by_id(self, id: int) -> None:
        query = 'DELETE FROM ' + self.CONTRACT_FIETS_TABLE + ' WHERE contract_fiets_id = %s'
        self._execute_and_commit_query(query, (id,))

    def insert(self, model : ContractFiets) -> int:
        query = 'INSERT INTO ' + self.CONTRACT_FIETS_TABLE + ' (contract_id, fiets_id) VALUES (%s, %s)'
        params = (model.contract_id, model.fiets_id)
        cursor = self._execute_and_commit_query(query, params)
        return int(cursor.lastrowid)

    def update(self, model : ContractFiets) -> None:
        query = 'UPDATE ' + self.CONTRACT_FIETS_TABLE + ' SET contract_id = %s, fiets_id = %s WHERE contract_fiets_id = %s'
        params = (model.contract_id, model.fiets_id, model.contract_fiets_id)
        self._execute_and_commit_query(query, params)

    def get_by_contract_id(self, contract_id: int) -> list[ContractFiets]:
        contract_fietsen_list = []

        query = 'SELECT * FROM ' + self.CONTRACT_FIETS_TABLE + ' WHERE contract_id = %s'

        for query_result in self._fetch_all(query, (contract_id,)):
            contract_fietsen_list.append(ContractFiets(query_result))

        return contract_fietsen_list
