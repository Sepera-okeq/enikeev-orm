"""
Модуль для работы с базой данных PostgreSQL.

Импорты:
    - Импортируются необходимые модули и библиотеки.

Классы:
    - Database: Класс для работы с базой данных PostgreSQL.

Методы:
    - __init__: Инициализация объекта базы данных и проверка её существования.
    - __enter__: Контекстный менеджер для открытия соединения с базой данных.
    - __exit__: Закрытие соединения с базой данных.
    - _ensure_database: Проверка существования и создание базы данных.
    - get_connection: Контекстный менеджер для получения соединения.
    - get_cursor: Контекстный менеджер для получения курсора.
    - create_db: Создание новой базы данных.
    - drop_db: Удаление базы данных.
    - clone_schema: Клонирование схемы из одной базы данных в другую.
    - create_dump: Создание дампа базы данных или таблицы.
    - restore_dump: Восстановление данных из дампа.
    - delete_all_data: Удаление всех данных из таблицы.
    - replace_all_data: Замена всех данных в таблице.
"""

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from contextlib import contextmanager
import subprocess
import os

class Database:
    """
    Класс для работы с базой данных PostgreSQL, включающий методы для создания, удаления, клонирования базы данных и работы с дампами.

    Атрибуты:
    - dbname (str): Имя базы данных.
    - user (str): Пользователь базы данных. По умолчанию 'postgres'.
    - password (str): Пароль пользователя базы данных.
    - host (str): Хост базы данных. По умолчанию 'localhost'.
    - port (int): Порт базы данных. По умолчанию 5432.

    Методы:
    - __init__: Инициализация объекта базы данных и проверка её существования.
    - __enter__: Контекстный менеджер для открытия соединения с базой данных.
    - __exit__: Закрытие соединения с базой данных.
    - _ensure_database: Проверка существования и создание базы данных.
    - get_connection: Контекстный менеджер для получения соединения.
    - get_cursor: Контекстный менеджер для получения курсора.
    - create_db: Создание новой базы данных.
    - drop_db: Удаление базы данных.
    - clone_schema: Клонирование схемы из одной базы данных в другую.
    - create_dump: Создание дампа базы данных или таблицы.
    - restore_dump: Восстановление данных из дампа.
    - delete_all_data: Удаление всех данных из таблицы.
    - replace_all_data: Замена всех данных в таблице.
    """

    def __init__(self, dbname, user='postgres', password='secret6g2h2', host='localhost', port=5432):
        """
        Инициализация объекта базы данных.

        :param dbname: Имя базы данных.
        :param user: Пользователь базы данных. По умолчанию 'postgres'.
        :param password: Пароль пользователя. По умолчанию 'secret6g2h2'.
        :param host: Хост базы данных. По умолчанию 'localhost'.
        :param port: Порт базы данных. По умолчанию 5432.
        """
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        # Проверка существования и создание базы данных
        self._ensure_database()

    def __enter__(self):
        """
        Открытие соединения с базой данных.

        :return: self
        """
        self.conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host, port=self.port)
        self.conn.autocommit = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Закрытие соединения с базой данных.
        """
        self.conn.close()

    def _ensure_database(self):
        """
        Проверка существования базы данных и создание её при отсутствии.
        """
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
    def get_connection(self):
        """
        Контекстный менеджер для получения соединения с базой данных.

        :yield: Соединение с базой данных.
        """
        conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host, port=self.port)
        conn.autocommit = True
        try:
            yield conn
        finally:
            conn.close()

    @contextmanager
    def get_cursor(self):
        """
        Контекстный менеджер для получения курсора.

        :yield: Курсор для выполнения SQL-запросов.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                yield cursor
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()

    def create_db(self, db_name):
        """
        Создание новой базы данных с заданным именем.

        :param db_name: Имя новой базы данных.
        """
        conn = psycopg2.connect(dbname='postgres', user=self.user, password=self.password, host=self.host, port=self.port)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        try:
            with conn.cursor() as cursor:
                create_db_sql = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
                cursor.execute(create_db_sql)
        except Exception as e:
            print(f"Error creating database: {e}")
        finally:
            conn.close()

    def drop_db(self, db_name):
        """
        Удаление базы данных с заданным именем.

        :param db_name: Имя базы данных для удаления.
        """
        with psycopg2.connect(dbname='postgres', user=self.user, password=self.password, host=self.host, port=self.port) as conn:
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            with conn.cursor() as cursor:
                cursor.execute(
                    sql.SQL("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname=%s AND pid <> pg_backend_pid()"),
                    [db_name]
                )

        conn = psycopg2.connect(dbname='postgres', user=self.user, password=self.password, host=self.host, port=self.port)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        try:
            with conn.cursor() as cursor:
                drop_db_sql = sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(db_name))
                cursor.execute(drop_db_sql)
        except Exception as e:
            print(f"Error dropping database: {e}")
        finally:
            conn.close()

    def clone_schema(self, source_db, target_db):
        """
        Клонирование схемы из исходной базы данных в целевую базу данных.

        :param source_db: Имя исходной базы данных.
        :param target_db: Имя целевой базы данных.
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
        Создание дампа базы данных или заданной таблицы с использованием pg_dump.

        :param output_file: Имя файла для сохранения дампа.
        :param table_name: Имя таблицы для создания дампа (если None, создается дамп всей базы данных).
        """
        env = os.environ.copy()
        env['PGPASSWORD'] = self.password

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

        subprocess.run(cmd, env=env, check=True)

    def restore_dump(self, input_file, table_name=None):
        """
        Восстановление данных в базе данных из дампа с использованием pg_restore.

        :param input_file: Имя файла дампа.
        :param table_name: Имя таблицы для восстановления (если None, восстанавливается вся база данных).
        """
        env = os.environ.copy()
        env['PGPASSWORD'] = self.password

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

        subprocess.run(cmd, env=env, check=True)

    def delete_all_data(self):
        """
        Удаляет все данные из всех таблиц базы данных.
        """
        with self.get_cursor() as cursor:
            cursor.execute("""
                DO $$ DECLARE
                    r RECORD;
                BEGIN
                    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
                        EXECUTE 'DELETE FROM ' || quote_ident(r.tablename);
                    END LOOP;
                END $$;
            """)

    def delete_all_data(self, table_name):
        """
        Удаление всех данных из указанной таблицы.

        :param table_name: Имя таблицы.
        """
        with self.get_cursor() as cursor:
            cursor.execute(f"DELETE FROM {table_name}")

    def replace_all_data(self, table_name, data):
        """
        Замена всех данных в указанной таблице.

        :param table_name: Имя таблицы.
        :param data: Новые данные для вставки.
        """
        with self.get_cursor() as cursor:
            cursor.execute(f"DELETE FROM {table_name}")
            for row in data:
                columns = ', '.join(row.keys())
                values = ', '.join([f"'{str(v)}'" for v in row.values()])
                cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})")
