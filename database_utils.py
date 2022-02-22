import sqlite3
from loglib import log


class DatabaseUtils:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def close(self):
        """close sqlite3 connection"""
        self.connection.close()

    def execute(self, query: str, values: list):
        """execute a row of data to current cursor"""
        self.cursor.execute(query, values)

    def insert(self, table: str, values: list):
        """add many new data to database in one go"""
        query = 'INSERT INTO ' + table + ' VALUES (' + ("?," * len(values))
        query = query[:-1] + ');'

        log(query)
        log(values)
        self.execute(query, values)

    def create_table(self, table_name: str, table_dict: dict):
        """create a database table if it does not exist already"""
        """table_dict must be formalised like this : {'attribute1':[type,constraints,...]}"""
        query = "CREATE TABLE IF NOT EXISTS " + table_name + "("
        for key, values in table_dict.items():
            query += key + ' '
            for value in values:
                query += value + ' '
            query += ', '
        query = query[:-2] + ")"
        self.cursor.execute(query)

    def select(self, table, column='*', where=""):
        query = "SELECT " + column + " FROM " + table
        if where != "":
            query += " WHERE " + where
        query += ";"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def select_one(self, table, column='*', where=""):
        query = "SELECT " + column + " FROM " + table
        if where != "":
            query += " WHERE " + where
        query += ";"
        log(query)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def last_id(self, table):
        query = "SELECT * FROM " + table + " ORDER BY id DESC LIMIT 1"
        log(query)
        self.cursor.execute(query)
        last_id = self.cursor.fetchone()
        if last_id is None:
            return -1
        return int(last_id[0])

    def commit(self):
        """commit changes to database"""
        self.connection.commit()
