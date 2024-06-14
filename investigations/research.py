"""
Модуль для проведения исследования времени выполнения операций с базой данных.
"""

import sys
import os
import shutil

# Добавляем путь к родительской директории для корректного импорта модулей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import matplotlib.pyplot as plt
from timeit import timeit
from lib.data_generator import *
from lib.db import Database
from lib.orm import *

def init_database():
    """
    Инициализирует базу данных: дропает старую, создает новую и создает таблицы.
    """
    admin_db = Database(dbname='postgres', user='postgres', password='secret6g2h2')
    admin_db.drop_db('testdb')
    admin_db.create_db('testdb')
    admin_db.close()

    db = Database(dbname='testdb', user='postgres', password='secret6g2h2')
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
    db.close()

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
db = Database(dbname='testdb', user='postgres', password='secret6g2h2')
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
db = Database(dbname='testdb', user='postgres', password='secret6g2h2')
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
    db = Database(dbname='testdb', user='postgres', password='secret6g2h2')

    # Времена генерации данных для разных таблиц
    times_applications = [measure_generate_time(generate_applications, n) for n in range(100, 3000, 100)]
    times_users = [measure_generate_time(generate_users, n, [1,2,3]) for n in range(100, 3000, 100)]

    # Строим графики
    plot_graph(
        range(100, 3000, 100), times_applications,
        "Время генерации данных для Applications в зависимости от количества записей", 
        "Количество записей", "Время (секунд)", "generate_time_applications.png"
    )
    plot_graph(
        range(100, 3000, 100), times_users,
        "Время генерации данных для Users в зависимости от количества записей", 
        "Количество записей", "Время (секунд)", "generate_time_users.png"
    )

    db.close()

def research_insert_time():
    """
    Исследует и строит графики времени вставки данных.
    """
    db = Database(dbname='testdb', user='postgres', password='secret6g2h2')

    # Генерация данных
    applications_data = generate_applications(3000)
    users_data = generate_users(3000, [1])

    # Времена вставки данных
    times_applications = [measure_insert_time(db, Application, applications_data[:n]) for n in range(100, 3000, 100)]
    times_users = [measure_insert_time(db, Users, users_data[:n]) for n in range(100, 3000, 100)]

    # Строим графики
    plot_graph(
        range(100, 3000, 100), times_applications,
        "Время вставки данных для Applications в зависимости от количества записей", 
        "Количество записей", "Время (секунд)", "insert_time_applications.png"
    )
    plot_graph(
        range(100, 3000, 100), times_users,
        "Время вставки данных для Users в зависимости от количества записей", 
        "Количество записей", "Время (секунд)", "insert_time_users.png"
    )

    db.close()

def research_query_time():
    """
    Исследует и строит графики времени выполнения запросов.
    """
    db = Database(dbname='testdb', user='postgres', password='secret6g2h2')

    queries_and_labels = [
        ("SELECT * FROM application", "SELECT * FROM application"),
        ("SELECT * FROM users WHERE email LIKE 'a%'", "SELECT * FROM users WHERE email LIKE 'a%'"),
        ("SELECT * FROM modification WHERE app_id=1", "SELECT * FROM modification WHERE app_id=1"),
        ("INSERT INTO application (app_name) VALUES ('TestApp')", "INSERT INTO application"),
        ("DELETE FROM application WHERE app_name='TestApp'", "DELETE FROM application"),
        ("UPDATE users SET email='updated@example.com' WHERE user_id=1", "UPDATE users SET email"),
    ]

    sizes = range(100, 3000, 100)
    for query, label in queries_and_labels:
        times = [measure_query_time(db, query) for n in sizes]
        plot_graph(
            sizes, times,
            f'Время выполнения {label} в зависимости от количества записей', 
            'Количество записей', 'Время (секунд)', f'query_time_{label.replace(" ", "_")}.png'
        )

    db.close()

if __name__ == "__main__":
    init_database()
    research_generate_time()
    research_insert_time()
    research_query_time()