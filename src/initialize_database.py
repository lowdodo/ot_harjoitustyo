from database_connection import get_database_connection


def drop_tables(connection):
    """Poistaa tietokantataulut ennen uusien luomista."""
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS tasks;")
    cursor.execute("DROP TABLE IF EXISTS users;")
    connection.commit()


def create_tables(connection):
    """Luo tietokantataulut."""
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            type TEXT CHECK(type IN ('set_time', 'open_time', 'passive')),
            start_time TEXT,
            duration_minutes INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
    """)
    connection.commit()


def initialize_database():
    """Alustaa tietokantataulut."""
    connection = get_database_connection()
    drop_tables(connection)
    create_tables(connection)


if __name__ == "__main__":  # pragma: no cover
    initialize_database()
