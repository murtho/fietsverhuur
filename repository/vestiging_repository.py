from model.vestiging import Vestiging
from repository.abstract_repository import AbstractRepository

class VestigingRepository(AbstractRepository):
    VESTIGING_TABLE = 'vestiging'

    def get_all(self) -> list[Vestiging]:
        vestigingen_list = []

        query = 'SELECT * FROM ' + self.VESTIGING_TABLE
        for query_result in self._fetch_all(query):
            vestigingen_list.append(Vestiging(query_result))

        return vestigingen_list

    def get_by_id(self, id: int) -> Vestiging | None:
        query = 'SELECT * FROM ' + self.VESTIGING_TABLE + ' WHERE vestiging_id = %s'

        query_result = self._fetch_one(query, (id,))
        if query_result is None:
            return None

        return Vestiging(query_result)

    def delete_by_id(self, id: int) -> None:
        query = 'DELETE FROM ' + self.VESTIGING_TABLE + ' WHERE vestiging_id = %s'
        self._execute_and_commit_query(query, (id,))

    def insert(self, model: Vestiging) -> int:
        query = 'INSERT INTO ' + self.VESTIGING_TABLE + ' (naam) VALUES (%s)'
        params = (model.naam,)
        cursor = self._execute_and_commit_query(query, params)
        return int(cursor.lastrowid)

    def update(self, model: Vestiging) -> None:
        query = 'UPDATE ' + self.VESTIGING_TABLE + ' SET naam = %s WHERE vestiging_id = %s'
        params = (model.naam, model.vestiging_id)
        self._execute_and_commit_query(query, params)