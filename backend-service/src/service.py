import logging
from typing import List, Dict

from fastapi import FastAPI
from fastapi_health import health

from src.article import Article
from src.comment import Comment
from src.db_connector import DBConnector
from src.utils.logger import init_logging

logger = init_logging(logging.INFO, __file__)
logger.info("Starting FastAPI Backend Service")
DB_CONNECTOR = None

def db_connect() -> bool:
    """establishes Python Postgres DB connection 

    Raises:
        ConnectionError: Raises connection error when the Postgres server is unreachable
    """
    try:
        global DB_CONNECTOR
        DB_CONNECTOR = DBConnector(logging.DEBUG)
        logger.info("Established connection to Postgres DB")
        return True
    except:
        logger.warning("Couldn't establish connection to Postgres DB, restart Postgres container")
        return False

def is_database_online() -> Dict:
    """ Verifies if the backend service is up and 
        if it can connect to the Postgres service

    Returns:
        dict: a dictionary with the statuses of backend and Postgres
        If the backed is offline, we will get interal server error
    """
    if db_connect():
        return {"Backend Status": "Online", "Postgres Status": "Online"}

    return {"Backend Status": "Online", "Postgres Status": "Offline"}

db_connect()
app = FastAPI()

@app.get("/")
def homepage() -> str:
    """Homepage endpoint

    Returns:
        str: Returns basic information about the service
    """
    return "FastAPI Backend service - Homepage"

app.add_api_route("/health", health([is_database_online]),name="Status Check")



@app.get("/fetch/")
def fetch_rows()-> List:
    """endpoint responsible to fetch articles without commenting from the table and send to client

    Returns:
        List[Article]: articles without comments
    """
    return DB_CONNECTOR.fetch()


@app.get("/nrows/")
def fetch_total_rows()-> Dict:
    """endpoint responsible to fetch number of articles without commenting

    Returns:
        Number of articles without commenting
    """
    total_rows = DB_CONNECTOR.fetch_row_count()
    response = {"Количество статей без комментариев ":total_rows}
    return response


