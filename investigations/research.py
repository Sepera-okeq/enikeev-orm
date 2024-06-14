import matplotlib.pyplot as plt
from timeit import timeit
from lib.data_generator import generate_users, generate_modifications, generate_purchases, generate_checks, generate_hwids, generate_operations, generate_subscriptions, generate_tokens, generate_versions
from lib.db import Database
from lib.orm import Users, Modification, Purchase, Checks, HWID, Operation, Subscription, Token, Version

def measure_insert_time(db, generate_func, model_class, n):
    data = generate_func(n, [1])

    def insert_operation():
        for item_data in data:
            item = model_class(**item_data)
            item.save(db)
    
    setup = f"""
from lib.db import Database
db = Database(dbname='testdb', user='postgres', password='secret6g2h2')
"""

    time = timeit(insert_operation, setup=setup, number=1)
    return time

def plot_graph(x, y, title, xlabel, ylabel, filename):
    plt.figure()
    plt.plot(x, y, marker='o')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(filename)
    plt.close()

db = Database(dbname='testdb', user='postgres', password='secret6g2h2')
Users.create_table(db)
times = [measure_insert_time(db, generate_users, Users, n) for n in range(100, 1001, 100)]
plot_graph(range(100, 1001, 100), times, "Insert Time for Users vs Number of Records", "Number of Records", "Time (s)", "insert_time_users.png")

Modification.create_table(db)
times = [measure_insert_time(db, generate_modifications, Modification, n) for n in range(100, 1001, 100)]
plot_graph(range(100, 1001, 100), times, "Insert Time for Modifications vs Number of Records", "Number of Records", "Time (s)", "insert_time_modifications.png")

# Следующие таблицы аналогично
db.close()