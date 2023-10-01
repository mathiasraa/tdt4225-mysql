from utils.data import get_trajectories_df, get_user_ids, get_labeled_ids, get_activities_df
from utils.connection import MySQLConnector
from tabulate import tabulate

def migrate():
    print("Migrating...")

    trajectories = get_trajectories_df("000")

def createUserTable():
    """Creates 'UserTable' SQL table with two columns['id' (VARCHAR(3)), 'has_label' (TINYINT)]
    
    """
    connection = MySQLConnector()
    cursor = connection.cursor
    db_connection = connection.db_connection
    table_name = "UserTable" #defines the name of the table

    query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
            id VARCHAR(3),
            has_label TINYINT(1)
        )
    """

    cursor.execute(query)
    db_connection.commit()

    data_to_insert = []

    for user in get_user_ids():
        if user in get_labeled_ids():
            data_to_insert.append((user, 1))
        else:
            data_to_insert.append((user, 0))

    insert_query = f"INSERT INTO {table_name} (id, has_label) VALUES (%s, %s)"
    cursor.executemany(insert_query, data_to_insert)
    db_connection.commit()

    '''
    print(f"{table_name} Contents")
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    print(tabulate(rows, headers=cursor.column_names))
    '''
    connection.close_connection()

if __name__ == "__main__":
    migrate()
    createUserTable()
