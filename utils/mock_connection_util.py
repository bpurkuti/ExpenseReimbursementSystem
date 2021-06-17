from psycopg2 import connect, OperationalError
import os


def create_connection():
    try:
        conn = connect(
            host="host",
            database="database",
            user="user",
            password="password",
            port=0000,
        )
        return conn
    except OperationalError as e:
        print(e)


connection = create_connection()
print(connection)
