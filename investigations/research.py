"""
Модуль для проведения исследования времени выполнения операций с базой данных.
"""

import sys
import os
from timeit import timeit

import matplotlib.pyplot as plt

# Добавляем путь к родительской директории для корректного импорта модулей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.db import Database
from lib.orm import Application, Users, Modification, Purchase, Checks, HWID, Operation, Subscription, Token, Version
from lib.data_generator import *
from lib.plot_utils import save_plot

def setup_sandbox(db_name):
    # Создание песочницы
    with Database("postgres", user="postgres", password="secret6g2h2") as db:
        db.drop_db(db_name)
        db.create_db(db_name)
        db.clone_schema("testdb", db_name)
    return Database(db_name, user="postgres", password="secret6g2h2")

def test_create_tables(db):
    Application.create_table(db)
    Users.create_table(db)
    Modification.create_table(db)
    Purchase.create_table(db)
    Checks.create_table(db)
    HWID.create_table(db)
    Operation.create_table(db)
    Subscription.create_table(db)
    Token.create_table(db)
    Version.create_table(db)

def test_insert_data(db):
    app_ids = [1, 2, 3]
    for app in generate_application_data(10):
        app.save(db)
    
    for user in generate_user_data(100, app_ids):
        user.save(db)

    for mod in generate_modification_data(50, app_ids):
        mod.save(db)

    user_ids = app_ids
    mod_ids = [1]
    for purchase in generate_purchase_data(100, user_ids, mod_ids):
        purchase.save(db)
    
    for check in generate_check_data(100, mod_ids):
        check.save(db)
    
    for hwid in generate_hwid_data(100, user_ids):
        hwid.save(db)
    
    for operation in generate_operation_data(100, user_ids):
        operation.save(db)
    
    for subscription in generate_subscription_data(100, user_ids, mod_ids):
        subscription.save(db)
    
    for token in generate_token_data(100, user_ids, mod_ids):
        token.save(db)
    
    for version in generate_version_data(100, mod_ids):
        version.save(db)

def test_dump_and_restore(db, dump_file):
    db.create_dump(dump_file)
    db.delete_all_data("application")
    db.restore_dump(dump_file, "application")

def measure_generate_time(model_class, n, *args):
    """
    Измеряет время генерации данных.
    """
    data_gen = {
        Application: generate_application_data,
        Users: generate_user_data,
        Modification: generate_modification_data,
        Purchase: generate_purchase_data,
        Checks: generate_check_data,
        HWID: generate_hwid_data,
        Operation: generate_operation_data,
        Subscription: generate_subscription_data,
        Token: generate_token_data,
        Version: generate_version_data
    }[model_class]

    setup = f"""
from lib.data_generator import {data_gen.__name__}
n = {n}
args = {args}
"""
    stmt = f"""
list({data_gen.__name__}(n, *args))
"""
    globals_dict = globals().copy()
    globals_dict.update({"n": n, "args": args})
    time = timeit(stmt, setup=setup, number=1, globals=globals_dict)
    return time

def measure_insert_time(db, model_class, n, *args):
    """
    Измеряет время вставки данных.
    """
    data_gen = {
        Application: generate_application_data,
        Users: generate_user_data,
        Modification: generate_modification_data,
        Purchase: generate_purchase_data,
        Checks: generate_check_data,
        HWID: generate_hwid_data,
        Operation: generate_operation_data,
        Subscription: generate_subscription_data,
        Token: generate_token_data,
        Version: generate_version_data
    }[model_class]

    def insert_operation():
        for item in data_gen(n, *args):
            item.save(db)
    
    setup = f"""
from lib.db import Database
db = Database(dbname='sandbox_testdb', user='postgres', password='secret6g2h2')
n = {n}
args = {args}
"""
    globals_dict = globals().copy()
    globals_dict.update({"db": db, "model_class": model_class, "data_gen": data_gen, "n": n, "args": args})
    time = timeit(insert_operation, setup=setup, number=1, globals=globals_dict)
    return time

def measure_query_time(db, query):
    """
    Измеряет время выполнения запроса.
    """
    setup = f"""
from lib.db import Database
db = Database(dbname='sandbox_testdb', user='postgres', password='secret6g2h2')
query = {repr(query)}
"""
    stmt = f"""
with db.get_cursor() as cur:
    cur.execute(query)
"""
    globals_dict = globals().copy()
    globals_dict.update({"query": query})
    time = timeit(stmt, setup=setup, number=1, globals=globals_dict)
    return time

def research_generate_time():
    """
    Исследует и строит графики времени генерации данных.
    """
    x_values = [range(100, 3001, 100)] * 2  # Копируем x_values для каждой линии
    y_values = []
    labels = ["Applications", "Users"]

    # Времена генерации данных для разных таблиц
    y_values.append([measure_generate_time(Application, n) for n in range(100, 3001, 100)])
    y_values.append([measure_generate_time(Users, n, [1,2,3,4,5,6,7,8,9,10]) for n in range(100, 3001, 100)])

    # Строим графики
    save_plot(
        x_values, y_values, labels,
        "Время генерации данных для различных моделей в зависимости от количества записей", 
        "Количество записей", "Время (секунд)", "generate_time_models",
    )

def research_insert_time():
    """
    Исследует и строит графики времени вставки данных.
    """
    x_values = [range(100, 3001, 100)] * 2  # Копируем x_values для каждой линии
    y_values = []
    labels = ["Applications", "Users"]

    with setup_sandbox("sandbox_testdb") as db:
        # Времена вставки данных
        y_values.append([measure_insert_time(db, Application, n) for n in range(100, 3001, 100)])
        y_values.append([measure_insert_time(db, Users, n, [1,2,3,4,5,6,7,8,9,10]) for n in range(100, 3001, 100)])

    # Строим графики
    save_plot(
        x_values, y_values, labels,
        "Время вставки данных для различных моделей в зависимости от количества записей", 
        "Количество записей", "Время (секунд)", "insert_time_models",
    )

def research_query_time():
    """
    Исследует и строит графики времени выполнения запросов.
    """
    x_values = [range(100, 3001, 100)] * 6  # Копируем x_values для каждой линии
    y_values = []
    labels = [
        "SELECT * FROM application",
        "SELECT * FROM users WHERE email LIKE 'a%'",
        "SELECT * FROM modification WHERE app_id=1",
        "INSERT INTO application",
        "DELETE FROM application",
        "UPDATE users SET email"
    ]

    with setup_sandbox("sandbox_testdb") as db:

        queries = [
            "SELECT * FROM application",
            "SELECT * FROM users WHERE email LIKE 'a%'",
            "SELECT * FROM modification WHERE app_id=1",
            "INSERT INTO application (app_name) VALUES ('TestApp')",
            "DELETE FROM application WHERE app_name='TestApp'",
            "UPDATE users SET email='updated@example.com' WHERE user_id=1"
        ]

        for query in queries:
            y_values.append([measure_query_time(db, query) for n in range(100, 3001, 100)])

    # Строим графики
    save_plot(
        x_values, y_values, labels,
        "Время выполнения запросов в зависимости от количества записей", 
        "Количество записей", "Время (секунд)", "query_time_models",
    )

def main():
    sandbox_name = "sandbox_testdb"
    dump_file = "test_dump.sql"

    # Настройка песочницы
    with setup_sandbox(sandbox_name) as db:

        # Тестирование создания таблиц
        test_create_tables(db)

        # Тестирование вставки данных
        test_insert_data(db)

        # Тестирование создания дампов и восстановления данных
        test_dump_and_restore(db, dump_file)

    # Очистка песочницы
    with Database("postgres", user="postgres", password="secret6g2h2") as db:
        db.drop_db(sandbox_name)

    if os.path.exists(dump_file):
        os.remove(dump_file)

    # Выполнение исследований
    research_generate_time()
    research_insert_time()
    research_query_time()

if __name__ == "__main__":
    main()