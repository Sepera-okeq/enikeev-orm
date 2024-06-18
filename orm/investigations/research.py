"""
Модуль для исследования производительности различных моделей и операций.

Импорты:
    - Подключаются необходимые модули и библиотеки для работы и визуализации данных.

Функции:
    - setup_sandbox: Создает песочницу для тестирования.
    - generate_data_for_table: Генерация данных для таблиц.
    - get_primary_key_name: Извлечение имени первичного ключа модели.
    - perform_queries: Выполнение различных запросов для замера времени.
    - measure_generate_time: Измерение времени генерации данных.
    - measure_insert_time: Измерение времени вставки данных.
    - measure_query_time: Измерение времени выполнения SQL-запроса.
    - measure_generation_times: Замер времени генерации данных.
    - measure_query_times: Замер времени выполнения запросов.
    - plot_results: Построение и сохранение графика с несколькими линиями.
    - plot_individual_query_times: Построение графиков времени выполнения запросов.
"""

import re
import sys
import os

# Добавляем путь к родительской директории для корректного импорта модулей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import timeit
import matplotlib.pyplot as plt
from lib.data_generator import (
    generate_application_data, generate_user_data, generate_modification_data, generate_purchase_data, 
    generate_check_data, generate_hwid_data, generate_operation_data, generate_subscription_data, 
    generate_token_data, generate_version_data
)
from lib.db import Database
from lib.orm import Application, Users, Modification, Purchase, Checks, HWID, Operation, Subscription, Token, Version, Model
from lib.plot_utils import save_plot

# Настройка параметров исследования
DATABASE_NAME = 'research_db'
TABLES = [Application, Users, Modification, Purchase, Checks, HWID, Operation, Subscription, Token, Version]
ROW_COUNTS = list(range(10, 501, 35))
REPEAT = 3  # Количество повторов для каждого замера

def setup_sandbox(db_name):
    """
    Создает песочницу для тестирования.

    :param db_name: Имя базы данных песочницы.
    :return: Объект Database с именем песочницы.
    """
    with Database("postgres", user="postgres", password="secret6g2h2") as db:
        db.drop_db(db_name)
        db.create_db(db_name)
        db.clone_schema("source_db", db_name)
    return Database(db_name, user="postgres", password="secret6g2h2")

# Функции для генерации данных
def generate_data_for_table(table, count):
    """
    Генерация данных для заданной таблицы.

    :param table: Класс модели таблицы.
    :param count: Количество записей для генерации.
    :return: Список объектов модели.
    """
    generator_map = {
        Application: generate_application_data,
        Users: lambda n: generate_user_data(n, [1]),
        Modification: lambda n: generate_modification_data(n, [1]),
        Purchase: lambda n: generate_purchase_data(n, [1], [1]),
        Checks: lambda n: generate_check_data(n, [1]),
        HWID: lambda n: generate_hwid_data(n, [1]),
        Operation: lambda n: generate_operation_data(n, [1]),
        Subscription: lambda n: generate_subscription_data(n, [1], [1]),
        Token: lambda n: generate_token_data(n, [1], [1]),
        Version: lambda n: generate_version_data(n, [1])
    }
    return list(generator_map[table](count))

# Функция для извлечения имени первичного ключа
def get_primary_key_name(model_class):
    """
    Извлечение имени первичного ключа для модели.

    :param model_class: Класс модели.
    :return: Имя первичного ключа.
    """
    docstring = model_class.__doc__
    if docstring:
        field_definitions = re.findall(
            r'(\w+): FieldType\.(\w+)(, primary_key=True)?',
            docstring
        )
        for field_name, field_type, primary_key in field_definitions:
            if primary_key:
                return field_name
    raise ValueError(f"No primary key found for model {model_class.__name__}")

# Функции для выполнения запросов
def perform_queries(db, table):
    """
    Выполнение различных SQL-запросов для оценки производительности.

    :param db: Объект Database для подключения к базе данных.
    :param table: Класс модели таблицы.
    :return: Список временных характеристик выполнения запросов.
    """
    primary_key = get_primary_key_name(table)
    
    data = generate_data_for_table(table, 1)[0]  # Генерировать одну запись для вставки
    
    results = []
    
    # Время на вставку (INSERT)
    # INSERT INTO {table.__name__.lower()} ({', '.join(data.extract_field_values()[0])}) VALUES ({', '.join(['%s'] * len(data.extract_field_values()[0]))}) RETURNING *;"
    start_time = timeit.default_timer()
    data.save(db)
    duration = timeit.default_timer() - start_time
    results.append(duration)
    
    # Время на выборку всех записей (SELECT all)
    # SELECT * FROM {table.__name__.lower()}
    start_time = timeit.default_timer()
    records = table.get_all(db)
    duration = timeit.default_timer() - start_time
    results.append(duration)
    
    # Время на подсчёт записей (SELECT COUNT(*))
    # SELECT COUNT(*) FROM {table.__name__.lower()}
    start_time = timeit.default_timer()
    count = len(records)
    duration = timeit.default_timer() - start_time
    results.append(duration)
    
    # Время на выборку по условию, которое не подходит ни для одной записи
    # SELECT * FROM {table.__name__.lower()} WHERE {primary_key} = %s"
    start_time = timeit.default_timer()
    no_match = table.filter(db, **{primary_key: -1})
    duration = timeit.default_timer() - start_time
    results.append(duration)
    
    # Время на выборку по определённому первичному ключу
    if records:
        match_id = getattr(records[0], primary_key)
        start_time = timeit.default_timer()
        match = table.filter(db, **{primary_key: match_id})
        duration = timeit.default_timer() - start_time
        results.append(duration)
    
        # Время на обновление (UPDATE)
        if match and len(records[0].__dict__.keys()) > 1:
            updated_field = {list(records[0].__dict__.keys())[1]: "temp_value"}  # обновление второго поле в объекте
            start_time = timeit.default_timer()
            match[0].update(db, **updated_field)
            duration = timeit.default_timer() - start_time
            results.append(duration)
    
        # Время на удаление записи (DELETE)
        if match:
            start_time = timeit.default_timer()
            match[0].delete(db)
            duration = timeit.default_timer() - start_time
            results.append(duration)
    
    # Время на выборку по определённому первичному ключу при помощи rawsql
    records = table.get_all(db)
    if records:
        match_id = getattr(records[0], primary_key)
        start_time = timeit.default_timer()
        Model.rawsql(db, f"SELECT * FROM {table.__name__.lower()} WHERE {primary_key} = %s", (match_id,))
        duration = timeit.default_timer() - start_time
        results.append(duration)
        
        # Время на обновление (UPDATE) при помощи rawsql
        start_time = timeit.default_timer()
        Model.rawsql(db, f"UPDATE {table.__name__.lower()} SET {list(records[0].__dict__.keys())[1]} = %s WHERE {primary_key} = %s", ("1", match_id))
        duration = timeit.default_timer() - start_time
        results.append(duration)
        
        # Время на удаление (DELETE) при помощи rawsql
        start_time = timeit.default_timer()
        Model.rawsql(db, f"DELETE FROM {table.__name__.lower()} WHERE {primary_key} = %s", (match_id,))
        duration = timeit.default_timer() - start_time
        results.append(duration)
    
    return results

def measure_generate_time(model_class, n):
    """
    Измеряет время генерации данных для модели.

    :param model_class: Класс модели.
    :param n: Количество генерируемых записей.
    :return: Время генерации данных.
    """
    data_gen_map = {
        Application: lambda n: generate_application_data(n),
        Users: lambda n: generate_user_data(n, [1]),
        Modification: lambda n: generate_modification_data(n, [1]),
        Purchase: lambda n: generate_purchase_data(n, [1], [1]),
        Checks: lambda n: generate_check_data(n, [1]),
        HWID: lambda n: generate_hwid_data(n, [1]),
        Operation: lambda n: generate_operation_data(n, [1]),
        Subscription: lambda n: generate_subscription_data(n, [1], [1]),
        Token: lambda n: generate_token_data(n, [1], [1]),
        Version: lambda n: generate_version_data(n, [1])
    }

    def generate_data():
        list(data_gen_map[model_class](n))

    time = timeit.timeit(generate_data, number=1)
    return time

def measure_insert_time(db, model_class, n):
    """
    Измеряет время вставки данных для модели.

    :param db: Объект Database для подключения к базе данных.
    :param model_class: Класс модели.
    :param n: Количество вставляемых записей.
    :return: Время вставки данных.
    """
    data_gen_map = {
        Application: lambda n: generate_application_data(n),
        Users: lambda n: generate_user_data(n, [1]),
        Modification: lambda n: generate_modification_data(n, [1]),
        Purchase: lambda n: generate_purchase_data(n, [1], [1]),
        Checks: lambda n: generate_check_data(n, [1]),
        HWID: lambda n: generate_hwid_data(n, [1]),
        Operation: lambda n: generate_operation_data(n, [1]),
        Subscription: lambda n: generate_subscription_data(n, [1], [1]),
        Token: lambda n: generate_token_data(n, [1], [1]),
        Version: lambda n: generate_version_data(n, [1])
    }

    def insert_operation():
        for item in data_gen_map[model_class](n):
            item.save(db)

    time = timeit.timeit(insert_operation, number=1)
    return time

def measure_query_time(db, query):
    """
    Измеряет время выполнения SQL-запроса.

    :param db: Объект Database для подключения к базе данных.
    :param query: SQL-запрос для выполнения.
    :return: Время выполнения запроса.
    """
    def execute_query():
        with db.get_cursor() as cur:
            cur.execute(query)

    time = timeit.timeit(execute_query, number=1)
    return time

def measure_generation_times():
    """
    Замеряет время генерации данных для всех таблиц и различных размеров данных.

    :return: Словарь с результатами замеров времени генерации данных.
    """
    results = {}
    for table in TABLES:
        times_per_size = []
        for count in ROW_COUNTS:
            duration_sum = 0
            for _ in range(REPEAT):
                duration = measure_generate_time(table, count)
                duration_sum += duration
            avg_duration = duration_sum / REPEAT
            times_per_size.append(avg_duration)
        results[table.__name__] = times_per_size
    return results

def measure_query_times():
    """
    Замеряет время выполнения различных запросов для всех таблиц и различных размеров данных.

    :return: Словарь с результатами замеров времени выполнения запросов.
    """
    db = setup_sandbox(DATABASE_NAME)
    results = {}
    for table in TABLES:
        times_per_size = {}
        for count in ROW_COUNTS:
            # Замените данные в таблице заданного количества строк
            data = generate_data_for_table(table, count)
            with db.get_cursor() as cur:
                table_name = table.__name__.lower()
                cur.execute(f'DELETE FROM {table_name}')
                for record in data:
                    record.save(db)

            query_times = perform_queries(db, table)
            for i, query_time in enumerate(query_times):
                if i not in times_per_size:
                    times_per_size[i] = []
                times_per_size[i].append(query_time)
        results[table.__name__] = times_per_size
    return results

def plot_results(results, plot_title, x_label, y_label, filename):
    """
    Построение и сохранение графика с несколькими линиями.

    :param results: Словарь результатов, где ключ - название таблицы, значение - список времен.
    :param plot_title: Название графика.
    :param x_label: Подпись оси X.
    :param y_label: Подпись оси Y.
    :param filename: Имя файла для сохранения графика (без расширения).
    """
    labels = list(results.keys())
    x_values = ROW_COUNTS
    y_values = [results[label] for label in labels]
    
    save_plot(x_values, y_values, labels, plot_title, x_label, y_label, filename)

def plot_individual_query_times(results):
    """
    Построение графиков времени выполнения запросов для каждой таблицы.
    
    :param results: Словарь результатов выполнения запросов.
    """
    for table, times_per_size in results.items():
        for query_index, times in times_per_size.items():
            save_plot(ROW_COUNTS, [times], [f"Запрос {query_index}"], f"Время выполнения Запроса {query_index} для {table}", 'Количество строк', 'Время выполнения (с)', f"{table}_query_{query_index}_times")

# Основной исполнимый код
if __name__ == "__main__":
    # Замер времени генерации данных
    generation_times = measure_generation_times()
    plot_results(generation_times, "Время генерации", "Количество строк", "Время (s)", "generation_times")

    # Замер времени выполнения запросов
    query_times = measure_query_times()
    plot_individual_query_times(query_times)