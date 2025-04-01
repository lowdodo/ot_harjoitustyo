import pytest
from database_connection import get_database_connection
from initialize_database import initialize_database


@pytest.fixture(scope="function")
def test_db():
    connection = get_database_connection()
    initialize_database()
    yield connection
    connection.close()
