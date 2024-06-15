import psycopg2
from contextlib import contextmanager
import subprocess

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

    def clone_schema(self, source_db, target_db):
        """
        Клонирует схему из исходной базы данных в целевую базу данных.
        """
        source_conn = psycopg2.connect(dbname=source_db, user=self.user, password=self.password, host=self.host, port=self.port)
        target_conn = psycopg2.connect(dbname=target_db, user=self.user, password=self.password, host=self.host, port=self.port)
        
        source_conn.autocommit = True
        target_conn.autocommit = True
        
        source_cur = source_conn.cursor()
        target_cur = target_conn.cursor()

        source_cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
        tables = source_cur.fetchall()

        for table in tables:
            source_cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table[0]}'")
            columns = source_cur.fetchall()
            columns_def = ", ".join([f"{col[0]} {col[1]}" for col in columns])
            target_cur.execute(f"CREATE TABLE {table[0]} ({columns_def})")

        source_cur.close()
        target_cur.close()
        source_conn.close()
        target_conn.close()

    def create_dump(self, output_file, table_name=None):
        """
        Создает дамп базы данных или заданной таблицы с использованием pg_dump.
        """
        cmd = [
            'pg_dump',
            '-h', self.host,
            '-p', str(self.port),
            '-U', self.user,
            '-F', 'c',
            '-f', output_file,
            self.dbname
        ]
        if table_name:
            cmd += ['-t', table_name]
        
        subprocess.run(cmd, check=True)

    def restore_dump(self, input_file, table_name=None):
        """
        Восстанавливает данные в базе данных из дампа с использованием pg_restore.
        """
        cmd = [
            'pg_restore',
            '-h', self.host,
            '-p', str(self.port),
            '-U', self.user,
            '-d', self.dbname,
            '-c',  # Очищает базу данных перед восстановлением
        ]
        if table_name:
            cmd += ['-t', table_name]
        
        cmd += [input_file]
        
        subprocess.run(cmd, check=True)

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