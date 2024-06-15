import psycopg2
from contextlib import contextmanager

class Database:
    def __init__(self, dbname, user='postgres', password='secret6g2h2', host='localhost', port=5432):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        # Проверка и создание базы данных, если ее нет
        self._ensure_database()

        # Подключение к уже существующей или новой базе данных
        self.conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host, port=self.port)

    def _ensure_database(self):
        conn = psycopg2.connect(dbname='postgres', user=self.user, password=self.password, host=self.host, port=self.port)
        conn.autocommit = True
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{self.dbname}'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f'CREATE DATABASE "{self.dbname}"')
        
        cursor.close()
        conn.close()

    @contextmanager
    def get_cursor(self):
        cursor = self.conn.cursor()
        try:
            yield cursor
        except Exception as e:
            self.conn.rollback()
            raise e
        else:
            self.conn.commit()
        finally:
            cursor.close()

    def close(self):
        self.conn.close()

    def create_db(self, db_name):
        conn = psycopg2.connect(dbname='postgres', user=self.user, password=self.password, host=self.host, port=self.port)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE {db_name}")
        cursor.close()
        conn.close()

    def drop_db(self, db_name):
        conn = psycopg2.connect(dbname='postgres', user=self.user, password=self.password, host=self.host, port=self.port)
        conn.autocommit = True
        cursor = conn.cursor()
        # Завершение всех соединений с базой перед удалением
        cursor.execute(f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='{db_name}' AND pid <> pg_backend_pid()")
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
        cursor.close()
        conn.close()

    def create_dump(self, output_file, table_name=None):
        with self.get_cursor() as cursor:
            if table_name:
                cursor.execute(f"COPY {table_name} TO STDOUT WITH CSV HEADER")
            else:
                cursor.execute("COPY (SELECT table_name FROM information_schema.tables WHERE table_schema='public') TO STDOUT WITH CSV HEADER")
            with open(output_file, 'w') as f:
                cursor.copy_expert(f"COPY {table_name or 'public'} TO STDOUT WITH CSV HEADER", f)

    def restore_dump(self, input_file, table_name=None):
        with self.get_cursor() as cursor:
            with open(input_file, 'r') as f:
                cursor.copy_expert(f"COPY {table_name or 'public'} FROM STDIN WITH CSV HEADER", f)

    def delete_all_data(self, table_name):
        with self.get_cursor() as cursor:
            cursor.execute(f"DELETE FROM {table_name}")

    def replace_all_data(self, table_name, data):
        with self.get_cursor() as cursor:
            cursor.execute(f"DELETE FROM {table_name}")
            for row in data:
                columns = ', '.join(row.keys())
                values = ', '.join([f"'{str(v)}'" for v in row.values()])
                cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})")