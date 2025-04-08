from repositories.user_repository import user_repository
from entities.user import User


def test_creating_user_is_successful(test_db):
    user = User(username="testi2", password="testi2")
    created_user = user_repository.create(user)

    assert created_user.username == "testi2"

def test_find_all_users(test_db):
    user1 = User(username="user1", password="password1")
    user2 = User(username="user2", password="password2")
    user_repository.create(user1)
    user_repository.create(user2)

    users = user_repository.find_all()

    assert len(users) >= 2
    assert any(u.username == "user1" for u in users)
    assert any(u.username == "user2" for u in users)