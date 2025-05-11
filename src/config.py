import os
from dotenv import load_dotenv

dirname = os.path.dirname(__file__)
env_path = os.path.join(dirname, "..", ".env")

load_dotenv(dotenv_path=env_path)

DATABASE_FILENAME = os.getenv("DATABASE_FILENAME") or "database.sqlite"
TEST_DATABASE_FILENAME = os.getenv(
    "TEST_DATABASE_FILENAME") or "test_database.sqlite"

DATABASE_FILE_PATH = os.path.join(dirname, "..", "data", DATABASE_FILENAME)
TEST_DATABASE_FILE_PATH = os.path.join(
    dirname, "..", "data", TEST_DATABASE_FILENAME)
