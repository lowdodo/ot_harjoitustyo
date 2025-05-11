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
    """Class for handling the repository side for tasks of the day
    """

    def __init__(self, connection):
        """
        constructor for the class

        Args:
            connection: path for the file for tasks

        """
        self._connection = connection

    def create(self, task: Task):
        """creates a task to database

        returns the task

        """

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
        task.task_id = cursor.lastrowid

        return task

    def find_all_by_user_id(self, user_id):
        """finds all the tasks connected to certain user_id from the database

        returns the tasks

        """
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT * FROM tasks WHERE user_id = ?",
            (user_id,)
        )

        rows = cursor.fetchall()

        return list(map(get_task_by_row, rows))

    def delete_all(self):
        """empties the database

        """
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM tasks")
        self._connection.commit()

    def delete_task(self, task_id):
        """deletes a specific task by its id

        """
        cursor = self._connection.cursor()
        cursor.execute(
            "DELETE FROM tasks WHERE task_id = ?",
            (task_id,)
        )
        self._connection.commit()

    def update_start_time(self, task_id, new_start_time):
        """changes the starttime of a task in db

        """
        cursor = self._connection.cursor()
        cursor.execute(
            "UPDATE tasks SET start_time = ? WHERE task_id = ?",
            (new_start_time, task_id)
        )
        self._connection.commit()

    def update_task(self, task: Task):
        """changes an existing task in db

        """
        cursor = self._connection.cursor()
        cursor.execute(
            """
            UPDATE tasks
            SET name = ?, type = ?, start_time = ?, duration_minutes = ?
            WHERE task_id = ?
            """,
            (task.name, task.type, task.start_time,
             task.duration_minutes, task.task_id)
        )
        self._connection.commit()


task_repository = TaskRepository(get_database_connection())
