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
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def close(self):
        self.conn.close()

    def create_sandbox(self, sandbox_name):
        with self.get_cursor() as cur:
            cur.execute(f"DROP DATABASE IF EXISTS {sandbox_name}")
            cur.execute(f"CREATE DATABASE {sandbox_name}")

    def clone_schema(self, source_db, target_db):
        source_conn = psycopg2.connect(dbname=source_db, user=self.user, password=self.password, host=self.host, port=self.port)
        target_conn = psycopg2.connect(dbname=target_db, user=self.user, password=self.password, host=self.host, port=self.port)

        source_cur = source_conn.cursor()
        target_cur = target_conn.cursor()

        source_cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
        tables = source_cur.fetchall()

        for table in tables:
            source_cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table[0]}'")
            columns = source_cur.fetchall()
            columns_def = ", ".join([f"{col[0]} {col[1]}" for col in columns])
            target_cur.execute(f"CREATE TABLE {table[0]} ({columns_def})")

        source_conn.close()
        target_conn.commit()
        target_conn.close()
    
    def create_sandbox_with_schema(self, sandbox_name, schema_source_db):
        self.create_sandbox(sandbox_name)
        self.clone_schema(schema_source_db, sandbox_name)