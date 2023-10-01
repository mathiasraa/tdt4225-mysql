from DbConnector import DbConnector
from tabulate import tabulate

connection = DbConnector()
cursor = connection.cursor
db_connection = connection.db_connection


query = """
CREATE TABLE IF NOT EXISTS %s (
        id VARCHAR(3),
        has_label TINYINT(1)
    )
    """

cursor.execute(query % "User")
db_connection.commit()

cursor.execute("SHOW TABLES")
rows = cursor.fetchall()

print(tabulate(rows, headers=cursor.column_names))

connection.close_connection()