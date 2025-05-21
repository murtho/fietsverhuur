from repository.abstract_repository import AbstractRepository
from model.klant import Klant

class KlantRepository(AbstractRepository):
    KLANT_TABLE = 'klant'

    def get_all(self) -> list[Klant]:
        klanten_list = []

        query = 'SELECT * FROM ' + self.KLANT_TABLE
        for query_result in self._fetch_all(query):
            klanten_list.append(Klant(query_result))

        return klanten_list

    def get_by_id(self, id: int) -> Klant | None:
        query = 'SELECT * FROM ' + self.KLANT_TABLE + ' WHERE klant_id = %s'
        query_result = self._fetch_one(query, (id,))

        if query_result is None:
            return None

        return Klant(query_result)

    def delete_by_id(self, id: int) -> None:
        query = 'DELETE FROM ' + self.KLANT_TABLE + ' WHERE klant_id = %s'
        self._execute_and_commit_query(query, (id,))

    def insert(self, model: Klant) -> int:
        query = 'INSERT INTO ' + self.KLANT_TABLE + ' (voornaam, achternaam, straat, huisnummer, toevoeging, postcode, plaats) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        params = (model.voornaam, model.achternaam, model.straat, model.huisnummer, model.toevoeging, model.postcode, model.plaats)
        cursor = self._execute_and_commit_query(query, params)
        return int(cursor.lastrowid)

    def update(self, model: Klant) -> None:
        query = 'UPDATE ' + self.KLANT_TABLE + ' SET voornaam = %s, achternaam = %s WHERE klant_id = %s'
        params = (model.voornaam, model.achternaam, model.klant_id)
        self._execute_and_commit_query(query, params)

    def search(self, search_term: str) -> list[Klant]:
        klanten_list = []

        query = ('SELECT * FROM ' + self.KLANT_TABLE +
                 ' WHERE CONCAT_WS(\' \', voornaam, achternaam) LIKE %s' +
                 ' OR CONCAT_WS(\' \', straat, CONCAT(huisnummer, toevoeging)) LIKE %s' +
                 ' OR plaats LIKE %s')
        params = (search_term, search_term, search_term)
        for query_result in self._fetch_all(query, params):
            klanten_list.append(Klant(query_result))

        return klanten_list
