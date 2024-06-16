"""
Модуль для проведения исследования времени выполнения операций с базой данных.
"""

import sys
import os
import shutil
from timeit import timeit
import matplotlib.pyplot as plt

# Добавляем путь к родительской директории для корректного импорта модулей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.db import Database
from lib.orm import Application, Users, Modification, Purchase, Checks, HWID, Operation, Subscription, Token, Version
from lib.data_generator import *

def setup_sandbox(db_name):
    # Создание песочницы
    db = Database("postgres", user="postgres", password="secret6g2h2")
    db.drop_db(db_name)
    db.create_db(db_name)
    db.clone_schema("testdb", db_name)
    db.close()
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
"""
    stmt = f"""
list({data_gen.__name__}(n, *{args}))
"""
    time = timeit(stmt, setup=setup, number=1, globals=globals())
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

def plot_graph(x, y, title, xlabel, ylabel, filename):
    """
    Строит и сохраняет график.
    """
    l_title = max(len(title), len(xlabel), len(ylabel))
    fig, ax = plt.subplots(figsize=(l_title // 6, 6))
    plt.plot(x, y, marker='o')
    plt.title(title)
    plt.xlabel(f"{xlabel} (OX)")
    plt.ylabel(f"{ylabel} (OY)")
    plt.savefig(filename)
    plt.close()

def research_generate_time():
    """
    Исследует и строит графики времени генерации данных.
    """
    # Времена генерации данных для разных таблиц
    times_applications = [measure_generate_time(Application, n) for n in range(100, 3001, 100)]
    times_users = [measure_generate_time(Users, n, [1,2,3]) for n in range(100, 3001, 100)]

    # Строим графики
    plot_graph(
        range(100, 3001, 100), times_applications,
        "Время генерации данных для Applications в зависимости от количества записей", 
        "Количество записей", "Время (секунд)", "generate_time_applications.png"
    )
    plot_graph(
        range(100, 3001, 100), times_users,
        "Время генерации данных для Users в зависимости от количества записей", 
        "Количество записей", "Время (секунд)", "generate_time_users.png"
    )

def research_insert_time():
    """
    Исследует и строит графики времени вставки данных.
    """
    db = setup_sandbox("sandbox_testdb")

    # Времена вставки данных
    times_applications = [measure_insert_time(db, Application, n) for n in range(100, 3001, 100)]
    times_users = [measure_insert_time(db, Users, n, [1,2,3]) for n в диапазоне (100, 3001, 100)]

    # Строим графики
    plot_graph(
        диапазон (100, 3001, 100), times_applications,
        "Время вставки данных для Applications в зависимости от количества записей", 
        "Количество записей", "Время (секунд)", "insert_time_applications.png"
    )
    plot_graph(
        диапазон (100, 3001, 100), times_users,
        "Время вставки данных для Users в зависимости от количества записей", 
        "Количество записей", "Время (секунд)", "insert_time_users.png"
    )

    db.close()

def research_query_time():
    """
    Исследует и строит графики времени выполнения запросов.
    """
    db = setup_sandbox("sandbox_testdb")

    queries_and_labels = [
        ("SELECT * FROM application", "SELECT * FROM application"),
        ("SELECT * FROM users WHERE email LIKE 'a%'", "SELECT * FROM users WHERE email LIKE 'a%'"),
        ("SELECT * FROM modification WHERE app_id=1", "SELECT * FROM modification WHERE app_id=1"),
        ("INSERT INTO application (app_name) VALUES ('TestApp')", "INSERT INTO application"),
        ("DELETE FROM application WHERE app_name='TestApp'", "DELETE FROM application"),
        ("UPDATE users SET email='updated@example.com' WHERE user_id=1", "UPDATE users SET email"),
    ]

    sizes = range(100, 3001, 100)
    for query, label in queries_and_labels:
        times = [measure_query_time(db, query) for n в диапазоне (100, 3001, 100)]
        plot_graph(
            размеры, времена,
            f'Время выполнения {label} в зависимости от количества записей', 
            'Количество записей', 'Время (секунд)', f'query_time_{label.replace(" ", "_")}.png'
        )

    db.close()

def main():
    sandbox_name = "sandbox_testdb"
    dump_file = "test_dump.sql"

    # Настройка песочницы
    db = setup_sandbox(sandbox_name)

    # Тестирование создания таблиц
    test_create_tables(db)

    # Тестирование вставки данных
    test_insert_data(db)

    # Тестирование создания дампов и восстановления данных
    test_dump_and_restore(db, dump_file)

    db.close()

    # Очистка песочницы
    db = Database("postgres", user="postgres", password="secret6g2h2")
    db.drop_db(sandbox_name)
    db.close()

    if os.path.exists(dump_file):
        os.remove(dump_file)

    # Выполнение исследований
    research_generate_time()
    research_insert_time()
    research_query_time()
    
if __name__ == "__main__":
    main()