from utils.connection import MySQLConnector


def reset():
    """
    Warning: The actions of this function cannot be undone!

    Reset the database.
    """
    connection = MySQLConnector()
    cursor = connection.cursor
    db_connection = connection.db_connection

    # Drop tables
    cursor.execute("DROP TABLE IF EXISTS TrackPointTable")
    cursor.execute("DROP TABLE IF EXISTS ActivityTable")
    cursor.execute("DROP TABLE IF EXISTS UserTable")
    db_connection.commit()

    print("Database sucessfully reset.")

    # Close connection
    connection.close_connection()


if __name__ == "__main__":
    reset()
