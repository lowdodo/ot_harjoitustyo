from repositories.task_repository import task_repository
from entities.task import Task


def test_creating_settime_task_is_succesfull(test_db):
    task = Task(user_id="1", name="task1", type="set_time",
                start_time="10:00", duration_minutes="30")
    created_task = task_repository.create(task)

    assert created_task.name == "task1"
    assert created_task.type == "set_time"


def test_creating_opentime_task_is_succesfull(test_db):
    task = Task(user_id="1", name="task2",
                type="open_time", duration_minutes="30")
    created_task = task_repository.create(task)

    assert created_task.name == "task2"
    assert created_task.type == "open_time"


def test_creating_passive_task_is_succesfull(test_db):
    task = Task(user_id="1", name="task3",
                type="passive", duration_minutes="30")
    created_task = task_repository.create(task)

    assert created_task.name == "task3"
    assert created_task.type == "passive"


def test_fetch_all_tasks_by_user(test_db):
    task1 = Task(user_id="1", name="task1", type="set_time",
                 start_time="10:00", duration_minutes="30")
    task2 = Task(user_id="1", name="task2",
                 type="open_time", duration_minutes="30")
    task3 = Task(user_id="1", name="task3",
                 type="passive", duration_minutes="30")
    task_repository.create(task1)
    task_repository.create(task2)
    task_repository.create(task3)

    tasks = task_repository.find_all_by_user_id("1")

    assert len(tasks) >= 2
    assert any(t.name == "task1" for t in tasks)
    assert any(t.name == "task2" for t in tasks)
    assert any(t.name == "task3" for t in tasks)


def test_fetching_task_without_user(test_db):
    tasks = task_repository.find_all_by_user_id("no_user")
    assert not tasks


def test_tasks_are_user_specific(test_db):
    task1 = Task(user_id=1, name="user1_task",
                 type="passive", duration_minutes=20)
    task2 = Task(user_id=2, name="user2_task",
                 type="open_time", duration_minutes=30)
    task_repository.create(task1)
    task_repository.create(task2)

    user1_tasks = task_repository.find_all_by_user_id(1)
    user2_tasks = task_repository.find_all_by_user_id(2)
    assert all(t.user_id == 1 for t in user1_tasks)
    assert all(t.user_id == 2 for t in user2_tasks)


def test_delete_all_tasks(test_db):
    task1 = Task(user_id="1", name="task1", type="set_time",
                 start_time="10:00", duration_minutes="30")
    task2 = Task(user_id="1", name="task2",
                 type="open_time", duration_minutes="30")
    task_repository.create(task1)
    task_repository.create(task2)

    task_repository.delete_all()

    tasks = task_repository.find_all_by_user_id(1)
    assert len(tasks) == 0


def test_task_with_no_start_time(test_db):
    task = Task(user_id="2", name="task_no_start", type="open_time",
                start_time=None, duration_minutes="25")
    created = task_repository.create(task)

    assert created.start_time is None


def test_created_task_is_retrievable(test_db):
    task = Task(user_id="1", name="task4", type="set_time",
                start_time="09:00", duration_minutes="45")
    task_repository.create(task)

    tasks = task_repository.find_all_by_user_id("1")
    found_task = next((t for t in tasks if t.name == "task4"), None)

    assert found_task is not None
    assert found_task.start_time == "09:00"
    assert found_task.duration_minutes == 45


def test_find_no_tasks_for_existing_user(test_db):
    task = Task(user_id="1", name="task1", type="set_time",
                start_time="10:00", duration_minutes="30")
    task_repository.create(task)

    tasks = task_repository.find_all_by_user_id("2")
    assert len(tasks) == 0
