"""
Модуль для проведения исследования времени выполнения операций с базой данных.
"""

import sys
import os

# Добавляем путь к родительской директории для корректного импорта модулей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.db import Database
from lib.orm import *
from lib.data_generator import *
import matplotlib.pyplot as plt
from timeit import timeit

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
    applications = generate_applications(10)
    for app_data in applications:
        app = Application(**app_data)
        app.save(db)
    
    users = generate_users(100, [1,2,3])
    for user_data in users:
        user = Users(**user_data)
        user.save(db)

    modifications = generate_modifications(50, [1])
    for mod_data in modifications:
        mod = Modification(**mod_data)
        mod.save(db)

    purchases = generate_purchases(100, [1], [1])
    for purchase_data in purchases:
        purchase = Purchase(**purchase_data)
        purchase.save(db)
    
    checks = generate_checks(100, [1])
    for check_data in checks:
        check = Checks(**check_data)
        check.save(db)
    
    hwids = generate_hwids(100, [1])
    for hwid_data in hwids:
        hwid = HWID(**hwid_data)
        hwid.save(db)
    
    operations = generate_operations(100, [1])
    for operation_data in operations:
        operation = Operation(**operation_data)
        operation.save(db)
    
    subscriptions = generate_subscriptions(100, [1], [1])
    for subscription_data in subscriptions:
        subscription = Subscription(**subscription_data)
        subscription.save(db)
    
    tokens = generate_tokens(100, [1], [1])
    for token_data in tokens:
        token = Token(**token_data)
        token.save(db)
    
    versions = generate_versions(100, [1])
    for version_data in versions:
        version = Version(**version_data)
        version.save(db)

def test_dump_and_restore(db, dump_file):
    db.create_dump(dump_file)
    db.delete_all_data("application")
    db.restore_dump(dump_file, "application")

def measure_generate_time(generate_func, *args):
    """
    Измеряет время генерации данных.
    """
    setup = f"""
from lib.data_generator import {generate_func.__name__}
"""
    stmt = f"""
{generate_func.__name__}(*{args})
"""
    time = timeit(stmt, setup=setup, number=1, globals=globals())
    return time

def measure_insert_time(db, model_class, data):
    """
    Измеряет время вставки данных.
    """
    def insert_operation():
        for item_data in data:
            item = model_class(**item_data)
            item.save(db)
    
    setup = f"""
from lib.db import Database
db = Database(dbname='sandbox_testdb', user='postgres', password='secret6g2h2')
"""
    globals_dict = globals().copy()
    globals_dict.update({"db": db, "model_class": model_class, "data": data})
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
    times_applications = [measure_generate_time(generate_applications, n) for n in range(100, 3001, 100)]
    times_users = [measure_generate_time(generate_users, n, [1,2,3]) for n in range(100, 3001, 100)]

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

    # Генерация данных
    applications_data = generate_applications(3000)
    users_data = generate_users(3000, [1])

    # Времена вставки данных
    times_applications = [measure_insert_time(db, Application, applications_data[:n]) for n in range(100, 3001, 100)]
    times_users = [measure_insert_time(db, Users, users_data[:n]) for n in range(100, 3001, 100)]

    # Строим графики
    plot_graph(
        range(100, 3001, 100), times_applications,
        "Время вставки данных для Applications в зависимости от количества записей", 
        "Количество записей", "Время (секунд)", "insert_time_applications.png"
    )
    plot_graph(
        range(100, 3001, 100), times_users,
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
        times = [measure_query_time(db, query) for n in sizes]
        plot_graph(
            sizes, times,
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