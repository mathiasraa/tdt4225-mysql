from utils.data import (
    get_trajectories_df,
    get_user_ids,
    get_labeled_ids,
    get_activities_df,
)
from utils.connection import MySQLConnector
from mysql.connector.cursor import MySQLCursor
from mysql.connector.connection import MySQLConnection


def create_user_table(cursor: MySQLCursor, db_connection: MySQLConnection):
    """
    Creates 'UserTable' SQL table with two columns:
    - 'id' (VARCHAR(255))
    - 'has_label' (TINYINT)

    """

    # Create table
    table_name = "UserTable"

    query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
            id VARCHAR(255) NOT NULL,
            has_label TINYINT(1),
            PRIMARY KEY (id)
        )
    """

    cursor.execute(query)
    db_connection.commit()

    # Insert data
    data_to_insert = []

    for user in get_user_ids():
        if user in get_labeled_ids():
            data_to_insert.append((str(user), 1))
        else:
            data_to_insert.append((str(user), 0))

    insert_query = f"INSERT INTO {table_name} (id, has_label) VALUES (%s, %s)"
    cursor.executemany(insert_query, data_to_insert)
    db_connection.commit()


def create_activity_table(cursor: MySQLCursor, db_connection: MySQLConnection):
    """
    Creates 'ActivityTable' SQL table with the following columns:
    - 'id' (INT AUTO_INCREMENT NOT NULL PRIMARY KEY)
    - 'user_id' (VARCHAR(255) NOT NULL FOREIGN KEY)
    - 'start_date_time' (DATETIME)
    - 'end_date_time' (DATETIME)
    - 'transportation_mode' (VARCHAR(20))
    """

    # Create table
    table_name = "ActivityTable"

    query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
            id INT AUTO_INCREMENT NOT NULL,
            user_id VARCHAR(255) NOT NULL,
            start_date_time DATETIME,
            end_date_time DATETIME,
            transportation_mode VARCHAR(20),
            FOREIGN KEY (user_id) REFERENCES UserTable(id),
            PRIMARY KEY (id)
        )
    """

    cursor.execute(query)
    db_connection.commit()

    # Insert data
    user_ids = get_user_ids()
    data_to_insert = []

    for user in user_ids:
        activities_df = get_activities_df(user)

        for _, row in activities_df.iterrows():
            data_to_insert.append(
                (
                    row["id"],
                    row["user_id"],
                    row["start_date_time"],
                    row["end_date_time"],
                    row["transportation_mode"],
                )
            )

    insert_query = f"""
        INSERT INTO {table_name} (id, user_id, start_date_time, end_date_time, transportation_mode)
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.executemany(insert_query, data_to_insert)
    db_connection.commit()


def create_track_point_table(cursor: MySQLCursor, db_connection: MySQLConnection):
    """
    Creates 'TrackPointTable' SQL table with the following columns:
    - 'id' (INT AUTO_INCREMENT NOT NULL PRIMARY KEY)
    - 'activity_id' (INT NOT NULL FOREIGN KEY)
    - 'lat' (FLOAT)
    - 'lon' (FLOAT)
    - 'altitude' (FLOAT)
    - 'date_time' (DATETIME)
    """

    # Create table
    table_name = "TrackPointTable"

    query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
            id INT AUTO_INCREMENT NOT NULL,
            activity_id INT NOT NULL,
            lat FLOAT,
            lon FLOAT,
            altitude FLOAT,
            date_time DATETIME,
            FOREIGN KEY (activity_id) REFERENCES ActivityTable(id),
            PRIMARY KEY (id)
        )
    """

    cursor.execute(query)
    db_connection.commit()

    # Insert data
    user_ids = get_user_ids()
    data_to_insert = []

    for user in user_ids:
        trajectories_df = get_trajectories_df(user)

        for _, row in trajectories_df.iterrows():
            data_to_insert.append(
                (
                    row["activity_id"],
                    row["latitude"],
                    row["longitude"],
                    row["altitude"],
                    row["date_time"],
                )
            )

    insert_query = f"""
        INSERT INTO {table_name} (activity_id, lat, lon, altitude, date_time)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_query, data_to_insert)
    db_connection.commit()


def migrate():
    print("Migrating...")

    connection = MySQLConnector()
    cursor = connection.cursor
    db_connection = connection.db_connection

    create_user_table(cursor, db_connection)
    create_activity_table(cursor, db_connection)
    create_track_point_table(cursor, db_connection)

    # Close connection
    connection.close_connection()


if __name__ == "__main__":
    migrate()
