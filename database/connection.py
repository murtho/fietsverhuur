from config.database_config import DatabaseConfig

import mysql.connector

class Database:
    def __init__(self, config : DatabaseConfig):
        self.config = config.get_dictionary()
        self.connection = None

    def connect(self):
        if not self.connection or not self.connection.is_connected():
            self.connection = mysql.connector.connect(**self.config)

    def get_cursor(self):
        self.connect()
        return self.connection.cursor(dictionary=True)

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()