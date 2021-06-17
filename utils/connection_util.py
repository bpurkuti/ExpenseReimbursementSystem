from psycopg2 import connect, OperationalError
import os


def create_connection():
    try:
        conn = connect(
            # Might need to replace os.environ.get("Stuff") with database/host info
            host="database-1.cfkqzvm5hdd2.us-west-1.rds.amazonaws.com",
            database="postgres",
            user="bpurkuti",
            password="superhuman1",
            port=5432,
        )
        return conn
    except OperationalError as e:
        print(e)


connection = create_connection()
print(connection)
