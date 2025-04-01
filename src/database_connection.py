import sqlite3
import os
import sys
from config import DATABASE_FILE_PATH, TEST_DATABASE_FILE_PATH

IS_TEST_ENV = "pytest" in sys.modules or os.getenv("TESTING") == "1"

DB_PATH = TEST_DATABASE_FILE_PATH if IS_TEST_ENV else DATABASE_FILE_PATH


def get_database_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection
