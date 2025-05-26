from database.connection import Database
from abc import ABC

# Deze abstracte class definieert de interne methodes om verbinding met de database te leggen
# Deze basis functionaliteit is nodig voor alle repositories
class AbstractConnectionRepository(ABC):
    def __init__(self, db: Database):
        self.__db = db

    def __execute_query(self, query, params=None):
        cursor = self.__db.get_cursor()
        cursor.execute(query, params or ())
        return cursor

    def _execute_and_commit_query(self, query, params=None):
        cursor = self.__execute_query(query, params)
        self.__db.connection.commit()
        return cursor

    def _fetch_all(self, query, params=None):
        cursor = self.__execute_query(query, params)
        return cursor.fetchall()

    def _fetch_one(self, query, params=None):
        cursor = self.__execute_query(query, params)
        return cursor.fetchone()