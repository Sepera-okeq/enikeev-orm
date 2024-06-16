import os
from datetime import datetime, timedelta
from lib.db import Database
from lib.orm import (
    Application,
    Users,
    Modification,
    Purchase,
    Checks,
    HWID,
    Operation,
    Subscription,
    Token,
    Version
)
from lib.data_generator import (
    generate_application_data,
    generate_user_data,
    generate_modification_data,
    generate_purchase_data,
    generate_check_data,
    generate_hwid_data,
    generate_operation_data,
    generate_subscription_data,
    generate_token_data,
    generate_version_data
)

def create_source_db_and_tables():
    db_name = 'source_db'
    db = Database(db_name)

    # Cоздание таблиц
    Application.create_table(db)
    Modification.create_table(db)
    Users.create_table(db)
    Purchase.create_table(db)
    Checks.create_table(db)
    HWID.create_table(db)
    Operation.create_table(db)
    Subscription.create_table(db)
    Token.create_table(db)
    Version.create_table(db)

    # После создания всех таблиц создаем связи many-to-many для Users
    Users.create_many_to_many_tables(db)
    
    print(f"База данных '{db_name}' и таблицы успешно созданы.")

    return db

def generate_and_insert_data(db):
    print("Генерация данных...")

    # Генерация и вставка данных для Application
    apps = list(generate_application_data(10))
    for app in apps:
        app.save(db)
    app_ids = [app.app_id for app in Application.get_all(db)]
    print(f"Сгенерировано {len(app_ids)} приложений")

    # Генерация и вставка данных для Users
    users = list(generate_user_data(100, app_ids))
    for user in users:
        user.save(db)
    user_ids = [user.user_id for user in Users.get_all(db)]
    print(f"Сгенерировано {len(user_ids)} пользователей")

    # Генерация и вставка данных для Modification
    mods = list(generate_modification_data(50, app_ids))
    for mod in mods:
        mod.save(db)
    mod_ids = [mod.mod_id for mod in Modification.get_all(db)]
    print(f"Сгенерировано {len(mod_ids)} модификаций")

    # Генерация и вставка данных для Purchase
    purchases = list(generate_purchase_data(200, user_ids, mod_ids))
    for purchase in purchases:
        purchase.save(db)
    purchase_ids = [purchase.purchase_id for purchase in Purchase.get_all(db)]
    print(f"Сгенерировано {len(purchase_ids)} покупок")

    # Генерация и вставка данных для Checks
    checks = list(generate_check_data(200, purchase_ids))
    for chk in checks:
        chk.save(db)
    print(f"Сгенерировано {len(checks)} чеков")

    # Генерация и вставка данных для HWID
    hwids = list(generate_hwid_data(100, user_ids))
    for hw in hwids:
        hw.save(db)
    hwid_ids = [hw.hwid_id for hw in HWID.get_all(db)]
    print(f"Сгенерировано {len(hwid_ids)} HWID записей")

    # Генерация и вставка данных для Operation
    operations = list(generate_operation_data(300, user_ids))
    for operation in operations:
        operation.save(db)
    print(f"Сгенерировано {len(operations)} операций")
        
    # Генерация и вставка данных для Subscription
    subscriptions = list(generate_subscription_data(150, user_ids, mod_ids))
    for subscription in subscriptions:
        subscription.save(db)
    print(f"Сгенерировано {len(subscriptions)} подписок")
    
    # Генерация и вставка данных для Token
    tokens = list(generate_token_data(100, user_ids, hwid_ids))
    for token in tokens:
        token.save(db)
    print(f"Сгенерировано {len(tokens)} токенов")

    # Генерация и вставка данных для Version
    versions = list(generate_version_data(50, mod_ids))
    for version in versions:
        version.save(db)
    print(f"Сгенерировано {len(versions)} версий")

    print("Данные сгенерированы и успешно вставлены.")

def create_dump(db, output_file):
    db.create_dump(output_file)
    print(f"Дамп базы данных '{db.dbname}' создан в файле '{output_file}'.")

if __name__ == "__main__":
    # Шаг 1: Создание базы данных source_db и её таблиц
    source_db = create_source_db_and_tables()

    # Шаг 2: Генерация и вставка данных
    generate_and_insert_data(source_db)

    # Шаг 3: Создание дампа базы данных
    dump_file = 'source_db_dump.sql'
    create_dump(source_db, dump_file)