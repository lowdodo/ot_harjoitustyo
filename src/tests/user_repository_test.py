from repositories.user_repository import user_repository
from entities.user import User


def test_creating_user_is_successful(test_db):
    user = User(username="testi2", password="testi2")
    created_user = user_repository.create(user)

    assert created_user.username == "testi2"
