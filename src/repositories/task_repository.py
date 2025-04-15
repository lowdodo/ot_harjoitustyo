from entities.task import Task
from database_connection import get_database_connection


def get_task_by_row(row):
    return Task(
        task_id=row["task_id"],
        user_id=row["user_id"],
        name=row["name"],
        type=row["type"],
        start_time=row["start_time"],
        duration_minutes=row["duration_minutes"]
    ) if row else None


class TaskRepository:
    def __init__(self, connection):
        self._connection = connection

    def create(self, task: Task):
        cursor = self._connection.cursor()

        cursor.execute(
            """
            INSERT INTO tasks (user_id, name, type, start_time, duration_minutes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (task.user_id, task.name, task.type,
             task.start_time, task.duration_minutes)
        )

        self._connection.commit()

        return task

    def find_all_by_user_id(self, user_id):
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT * FROM tasks WHERE user_id = ?",
            (user_id,)
        )

        rows = cursor.fetchall()

        return list(map(get_task_by_row, rows))

    def delete_all(self):
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM tasks")
        self._connection.commit()

    def update_start_time(self, task_id, new_start_time):
        cursor = self._connection.cursor()
        cursor.execute(
            "UPDATE tasks SET start_time = ? WHERE task_id = ?",
            (new_start_time, task_id)
        )
        self._connection.commit()


task_repository = TaskRepository(get_database_connection())
