from entities.user import User
from entities.task import Task
from repositories.user_repository import user_repository as default_user_repository
from repositories.task_repository import task_repository as default_task_repository


class InvalidCredentialsError(Exception):
    pass


class UsernameExistsError(Exception):
    pass


class DayplanService:

    def __init__(self, user_repository=default_user_repository, task_repository=default_task_repository):

        self._user_repository = user_repository
        self._task_repository = task_repository
        self._user = None

    def login(self, username, password):
        print("ollaan loginissa")
        user = self._user_repository.find_by_username(username)

        if not user or user.password != password:
            raise InvalidCredentialsError("Invalid username or password")

        self._user = user
        print(f"Logged in as: {user.user_id}, {user.username}")
        return user

    def get_current_user(self):

        return self._user

    def get_users(self):

        return self._user_repository.find_all()

    def logout(self):
        self._user = None

    def create_user(self, username, password, login=True):
        existing_user = self._user_repository.find_by_username(username)

        if existing_user:
            raise UsernameExistsError(f"Username {username} already exists")

        user = self._user_repository.create(User(None, username, password))

        if login:
            self._user = user

        return user

    def create_task(self, task: Task):
        self._task_repository.create(task)

    def get_tasks_for_user(self, user_id):
        return self._task_repository.find_all_by_user_id(user_id)
