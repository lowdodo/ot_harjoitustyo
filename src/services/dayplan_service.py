from entities.user import User
from entities.task import Task
from repositories.user_repository import user_repository as default_user_repository
from repositories.task_repository import task_repository as default_task_repository


class InvalidCredentialsError(Exception):
    pass


class UsernameExistsError(Exception):
    pass


class DayplanService:
    """Class for app logic"""
    def __init__(self,
                 user_repository=default_user_repository,
                 task_repository=default_task_repository):
        """Constructor for the class, creates repositories for the service

        Args:
            user_repository: db for users
            task_repository: db for tasks
        """
        self._user_repository = user_repository
        self._task_repository = task_repository
        self._user = None

    def login(self, username, password):
        """Logs a user in to its account

        returns user if username and password matches to an existing user

        """
        user = self._user_repository.find_by_username(username)

        if not user or user.password != password:
            raise InvalidCredentialsError("Invalid username or password")

        self._user = user
        print(f"Logged in as: {user.user_id}, {user.username}")
        return user

    def get_current_user(self):
        """Gets the user now logged in

        returns user

        """

        return self._user

    def get_users(self):
        """Gets all the users in db

        returns all user-objects
        """

        return self._user_repository.find_all()

    def logout(self):
        """Logs out an user
        """
        self._user = None

    def create_user(self, username, password, login=True):
        """Creates a new user to db

        returns the user

        """
        existing_user = self._user_repository.find_by_username(username)

        if existing_user:
            raise UsernameExistsError(f"Username {username} already exists")

        user = self._user_repository.create(User(None, username, password))
        self._user = user

        return user

    def create_task(self, task: Task):
        """Creates a new task to db

        """
        self._task_repository.create(task)

    def get_tasks_for_user(self, user_id):
        """
        returns all the tasks connected to certain user_id in db

        """
        return self._task_repository.find_all_by_user_id(user_id)

    def update_task_start_time(self, task_id, new_start_time):
        """Updates the starting time of a specific task

        """
        self._task_repository.update_start_time(task_id, new_start_time)

    def update_task(self, task: Task):
        """Updates a specific task
        """
        self._task_repository.update_task(task)

    def delete_all_tasks_for_user(self, user_id):
        """deletes all the tasks from a specific user
        """
        tasks = self._task_repository.find_all_by_user_id(user_id)
        for task in tasks:
            self._task_repository.delete_task(task.task_id)
        print(f"All tasks for user {user_id} have been deleted.")
