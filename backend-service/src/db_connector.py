import os
import logging
from datetime import datetime
from typing import Union, Dict, List
from psycopg2 import connect, sql, DatabaseError

from src.utils.logger import init_logging

class DBConnector():
    """Class for communicating with the Postgres DB
    """
    def __init__(self, log_level:str = logging.INFO) -> None:
        self.logger = init_logging(log_level, __file__)
        self.conn = self._db_connect()

    def check_db_status(self) -> int:
        """to fetch the current status of the docker hosted Postgres service

        Returns:
            int: connection status code
        """
        return self.conn.status

    def _db_connect(self):
        """creates a connection to Postgres DB

        Returns:
            connection: DB connection based on psycopg2 module
        """
        username = os.environ['POSTGRES_USER']
        password = os.environ['POSTGRES_PASS']
        database = os.environ['POSTGRES_DB']
        hostname = os.environ['POSTGRES_HOST']
        port = os.environ['POSTGRES_PORT']

        conn = connect(
		host=hostname,
		port = port,
		dbname=database,
		user=username,
		password=password)
        return conn

    def fetch_row_count(self) -> int:
        """fetches total number of articles without commenting

        Returns:
            int: Total number of articles without commenting
        """

        query = sql.SQL("SELECT COUNT(1) FROM article LEFT JOIN comment ON article.id = comment.article_id WHERE comment.id is NULL;")

        return self.execute(query, None, "fetch")[0][0]

    def fetch(self, params: dict = None) -> List:
        """fetches all articles without commenting

        
        Returns:
            List: all articles without commenting
        """
        query = "SELECT article.id, article.title, article.text FROM article LEFT JOIN comment ON article.id = comment.article_id WHERE comment.id is NULL"
        return self.execute(query, None, "fetch")



    def execute(self, query:str, params:Union[Dict, None], query_type:str) -> list:
        """Executes the given SQL query

        Args:
            query (str): SQL query to execute

        Returns:
            list: inserted rows count for an insert query or
                  updated rows count for an update query or
                  deleted rows count for an update query or
                  list of records for a select query and few 
                  more results based on the type of DML operations
        """
        if self.conn.closed:
            self.conn = self._db_connect()
        cur = self.conn.cursor()
        try:
            cur.execute(query)

            if query_type == 'fetch':
                results = cur.fetchall()
            else:
                raise ValueError("Invalid query type")
            self.conn.commit()
            return results
        except (Exception, DatabaseError) as error:
            self.conn.rollback()
            raise DatabaseError("Error in transaction, reverting all changes using rollback ", error)
            
