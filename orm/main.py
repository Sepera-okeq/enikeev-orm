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
    """
    Создание базы данных 'source_db' и её таблиц.

    :return: Объект Database для созданной базы данных.
    """
    db_name = 'source_db'
    db = Database(db_name)

    # Создание таблиц для всех моделей
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

    # Создание таблиц many-to-many для Users после создания всех таблиц
    Users.create_many_to_many_tables(db)
    
    print(f"База данных '{db_name}' и таблицы успешно созданы.")
    return db

def generate_and_insert_data(db):
    """
    Генерация и вставка данных в базу данных.

    :param db: Объект Database для подключения к базе данных.
    """
    print("Генерация данных...")

    # Генерация и вставка данных для модели Application
    apps = list(generate_application_data(10))
    for app in apps:
        app.save(db)
    app_ids = [app.app_id for app in Application.get_all(db)]
    print(f"Сгенерировано {len(app_ids)} приложений")

    # Генерация и вставка данных для модели Users
    users = list(generate_user_data(100, app_ids))
    for user in users:
        user.save(db)
    user_ids = [user.user_id for user in Users.get_all(db)]
    print(f"Сгенерировано {len(user_ids)} пользователей")

    # Генерация и вставка данных для модели Modification
    mods = list(generate_modification_data(50, app_ids))
    for mod in mods:
        mod.save(db)
    mod_ids = [mod.mod_id for mod in Modification.get_all(db)]
    print(f"Сгенерировано {len(mod_ids)} модификаций")

    # Генерация и вставка данных для модели Purchase
    purchases = list(generate_purchase_data(200, user_ids, mod_ids))
    for purchase in purchases:
        purchase.save(db)
    purchase_ids = [purchase.purchase_id for purchase in Purchase.get_all(db)]
    print(f"Сгенерировано {len(purchase_ids)} покупок")

    # Генерация и вставка данных для модели Checks
    checks = list(generate_check_data(200, purchase_ids))
    for chk in checks:
        chk.save(db)
    print(f"Сгенерировано 200 чеков")

    # Генерация и вставка данных для модели HWID
    hwids = list(generate_hwid_data(100, user_ids))
    for hw in hwids:
        hw.save(db)
    hwid_ids = [hw.hwid_id for hw in HWID.get_all(db)]
    print(f"Сгенерировано {len(hwid_ids)} HWID записей")

    # Генерация и вставка данных для модели Operation
    operations = list(generate_operation_data(300, user_ids))
    for operation in operations:
        operation.save(db)
    print(f"Сгенерировано {len(operations)} операций")
        
    # Генерация и вставка данных для модели Subscription
    subscriptions = list(generate_subscription_data(150, user_ids, mod_ids))
    for subscription in subscriptions:
        subscription.save(db)
    print(f"Сгенерировано {len(subscriptions)} подписок")
    
    # Генерация и вставка данных для модели Token
    tokens = list(generate_token_data(100, user_ids, hwid_ids))
    for token in tokens:
        token.save(db)
    print(f"Сгенерировано {len(tokens)} токенов")

    # Генерация и вставка данных для модели Version
    versions = list(generate_version_data(50, mod_ids))
    for version in versions:
        version.save(db)
    print(f"Сгенерировано {len(versions)} версий")

    print("Данные сгенерированы и успешно вставлены.")

def create_dump(db, output_file):
    """
    Создание дампа базы данных и сохранение его в файл.

    :param db: Объект Database для подключения к базе данных.
    :param output_file: Имя файла для сохранения дампа.
    """
    db.create_dump(output_file)
    print(f"Дамп базы данных '{db.dbname}' создан в файле '{output_file}'.")

if __name__ == "__main__":
    db = create_source_db_and_tables()
    generate_and_insert_data(db)
    create_dump(db, "source_db_dump.sql")