from utils.data import (
    get_trajectories_df,
    get_user_ids,
    get_labeled_ids,
    get_activities_df,
)
from utils.connection import MySQLConnector
from tabulate import tabulate


def create_user_table(cursor, db_connection):
    """
    Creates 'UserTable' SQL table with two columns:
    - 'id' (VARCHAR(3))
    - 'has_label' (TINYINT)

    """

    # Create table
    table_name = "UserTable"

    query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
            id VARCHAR(3),
            has_label TINYINT(1)
        )
    """

    cursor.execute(query)
    db_connection.commit()

    # Insert data
    data_to_insert = []

    for user in get_user_ids():
        if user in get_labeled_ids():
            data_to_insert.append((user, 1))
        else:
            data_to_insert.append((user, 0))

    insert_query = f"INSERT INTO {table_name} (id, has_label) VALUES (%s, %s)"
    cursor.executemany(insert_query, data_to_insert)
    db_connection.commit()


def create_track_point_table():
    """
    Creates 'TrackPointTable' SQL table with the following columns:
    - 'id' (INT AUTO_INCREMENT NOT NULL PRIMARY KEY)
    - 'activity_id' (INT NOT NULL FOREIGN KEY)
    - 'lat' (FLOAT)
    - 'lon' (FLOAT)
    - 'altitude' (FLOAT)
    - 'date_time' (DATETIME)
    """

    user_ids = get_user_ids()


def migrate():
    print("Migrating...")

    connection = MySQLConnector()
    cursor = connection.cursor
    db_connection = connection.db_connection

    create_user_table(cursor, db_connection)

    # Close connection
    connection.close_connection()


if __name__ == "__main__":
    migrate()
