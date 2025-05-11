from entities.user import User
from database_connection import get_database_connection


def get_user_by_row(row):
    return User(row["user_id"], row["username"], row["password"]) if row else None


class UserRepository:
    """Class for handling the repository side for users in db
    """

    def __init__(self, connection):
        """constructor for the class

        Args:
            connection: path for the file that the users are saved
        """
        self._connection = connection

    def find_all(self):
        """Returns all users

        """
        cursor = self._connection.cursor()

        cursor.execute("select * from users")

        rows = cursor.fetchall()

        return list(map(get_user_by_row, rows))

    def find_by_username(self, username):
        """Returns user by its username

        """
        cursor = self._connection.cursor()

        cursor.execute(
            "select * from users where username = ?",
            (username,)
        )

        row = cursor.fetchone()

        return get_user_by_row(row)

    def create(self, user):
        """Creates a new user to db

        """
        cursor = self._connection.cursor()

        cursor.execute(
            "insert into users (username, password) values (?, ?)",
            (user.username, user.password)
        )

        self._connection.commit()

        return user

    def delete_all(self):
        """Deletes all users from db

        """
        cursor = self._connection.cursor()

        cursor.execute("delete from users")

        self._connection.commit()


user_repository = UserRepository(get_database_connection())
