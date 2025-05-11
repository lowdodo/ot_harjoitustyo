import pytest
from entities.user import User
from entities.task import Task
from services.dayplan_service import DayplanService, InvalidCredentialsError, UsernameExistsError


class MockUserRepo:
    def __init__(self):
        self.users = []

    def find_by_username(self, username):
        for u in self.users:
            if u.username == username:
                return u
        return None

    def create(self, user):
        user.user_id = len(self.users) + 1
        self.users.append(user)
        return user

    def find_all(self):
        return self.users

    def delete_all(self):
        self.users = []


class MockTaskRepo:
    def __init__(self):
        self.tasks = []

    def create(self, task):
        task.task_id = len(self.tasks) + 1
        self.tasks.append(task)
        return task

    def find_all_by_user_id(self, user_id):
        return [t for t in self.tasks if str(t.user_id) == str(user_id)]

    def update_start_time(self, task_id, new_start_time):
        for t in self.tasks:
            if t.task_id == task_id:
                t.start_time = new_start_time
                return

    def update_task(self, task):
        for idx, t in enumerate(self.tasks):
            if t.task_id == task.task_id:
                self.tasks[idx] = task
                return

    def delete_task(self, task_id):
        self.tasks = [t for t in self.tasks if t.task_id != task_id]

    def delete_all(self):
        self.tasks = []


@pytest.fixture
def user_repo():
    return MockUserRepo()


@pytest.fixture
def task_repo():
    return MockTaskRepo()


@pytest.fixture
def service(user_repo, task_repo):
    return DayplanService(user_repository=user_repo, task_repository=task_repo)


def test_create_user_is_successful(service, user_repo):
    user = service.create_user("testuser", "testpw")
    assert user.username == "testuser"
    assert service.get_current_user().username == "testuser"
    assert user_repo.find_by_username("testuser") is not None


def test_create_user_duplicate_raises(service, user_repo):
    user_repo.create(User(None, "exists", "pw"))
    with pytest.raises(UsernameExistsError):
        service.create_user("exists", "pw")


def test_login_success(service, user_repo):
    user_repo.create(User(None, "user1", "pw1"))
    user = service.login("user1", "pw1")
    assert user.username == "user1"
    assert service.get_current_user().username == "user1"


def test_login_invalid_credentials(service, user_repo):
    with pytest.raises(InvalidCredentialsError):
        service.login("nouser", "nopw")
    user_repo.create(User(None, "user1", "pw1"))
    with pytest.raises(InvalidCredentialsError):
        service.login("user1", "wrongpw")


def test_logout(service):
    service._user = User(1, "user1", "pw1")
    service.logout()
    assert service.get_current_user() is None


def test_get_users(service, user_repo):
    user_repo.create(User(None, "user1", "pw1"))
    user_repo.create(User(None, "user2", "pw2"))
    users = service.get_users()
    assert len(users) == 2
    assert users[0].username == "user1" or users[1].username == "user1"
    assert users[0].username == "user2" or users[1].username == "user2"


def test_create_task(service, task_repo):
    task = Task(user_id=1, name="task", type="set_time",
                start_time="10:00", duration_minutes=30)
    service.create_task(task)
    assert task_repo.tasks[0].name == "task"


def test_get_tasks_for_user(service, task_repo):
    task1 = Task(user_id=1, name="task1", type="set_time",
                 start_time="10:00", duration_minutes=30)
    task2 = Task(user_id=2, name="task2", type="open_time",
                 start_time=None, duration_minutes=20)
    task_repo.create(task1)
    task_repo.create(task2)
    tasks = service.get_tasks_for_user(1)
    assert len(tasks) == 1
    assert tasks[0].name == "task1"


def test_update_task_start_time(service, task_repo):
    task = Task(user_id=1, name="task", type="set_time",
                start_time="10:00", duration_minutes=30)
    created = task_repo.create(task)
    service.update_task_start_time(created.task_id, "09:00")
    assert task_repo.tasks[0].start_time == "09:00"


def test_update_task(service, task_repo):
    task = Task(user_id=1, name="task", type="set_time",
                start_time="10:00", duration_minutes=30)
    created = task_repo.create(task)
    created.duration_minutes = 45
    service.update_task(created)
    assert task_repo.tasks[0].duration_minutes == 45


def test_delete_all_tasks_for_user(service, task_repo):
    t1 = Task(user_id=1, name="t1", type="set_time",
              start_time="10:00", duration_minutes=30)
    t2 = Task(user_id=1, name="t2", type="open_time",
              start_time=None, duration_minutes=20)
    t3 = Task(user_id=2, name="t3", type="passive",
              start_time=None, duration_minutes=10)
    task_repo.create(t1)
    task_repo.create(t2)
    task_repo.create(t3)
    service.delete_all_tasks_for_user(1)
    assert all(t.user_id != 1 for t in task_repo.tasks)
