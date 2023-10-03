from tabulate import tabulate
from utils.connection import MySQLConnector
from mysql.connector.cursor import MySQLCursor
from mysql.connector.connection import MySQLConnection
import pandas as pd
from IPython.display import display


def inspection(cursor: MySQLCursor, db_connection: MySQLConnection):
    print("Inspection")

    cursor.execute("SHOW TABLES")
    rows = cursor.fetchall()
    print(tabulate(rows, headers=cursor.column_names))


def inspectionTables(cursor: MySQLCursor, db_connection: MySQLConnection):
    print("InspectionTables")

    # Ensure all columns are displayed
    pd.set_option("display.max_columns", None)

    specific_tables = ["UserTable", "ActivityTable", "TrackPointTable"]

    for table_name in specific_tables:
        # Checking if the table name exists in the database
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        result = cursor.fetchone()

        if result:  # If table exists
            # Printing the table name for clarity
            print(f"Table: {table_name}")

            # Fetching the table content using pandas
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, db_connection)

            # Displaying the first 5 rows of the DataFrame
            display(df.head())
            print("\n" + "-" * 50 + "\n")  # Separator between tables
        else:
            print(f"Table {table_name} not found in the database.")


if __name__ == "__main__":
    connection = MySQLConnector()
    cursor = connection.cursor
    db_connection = connection.db_connection

    inspectionTables(cursor, db_connection)

    connection.close_connection()
