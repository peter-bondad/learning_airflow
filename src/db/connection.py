import os
from psycopg2 import connect
from src.utils.logger import get_logger
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = get_logger(__name__)

# This module provides a function to establish a connection to the PostgreSQL database using credentials from environment variables.
def db_connect():

    try:
        logger.info("Connecting to the database...")
        return connect(
            host=os.getenv("DB_HOST"),  # local test
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            dbname=os.getenv("DB_NAME"),
        )
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")
        raise e
