import sys
import os
import shutil

# Добавляем путь к родительской директории для корректного импорта модулей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.db import Database
from lib.orm import *
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
    Database("postgres", user="postgres", password="secret6g2h2").drop_db(sandbox_name)
    if os.path.exists(dump_file):
        os.remove(dump_file)
    
if __name__ == "__main__":
    main()