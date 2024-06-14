from lib.db import Database
from lib.data_generator import *
from lib.orm import *

def main():
    # Создание или подключение к основной базе данных
    db = Database(dbname='testdb')  # Автоматически создается, если не существует
    
    # Создание таблиц
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

    # Генерация и вставка данных
    applications = generate_applications(10)
    for app_data in applications:
        app = Application(**app_data)
        app.save(db)
    
    # Получаем id созданных приложений
    app_ids = [app.app_id for app in Application.get_all(db)]

    users = generate_users(100, app_ids)
    for user_data in users:
        user = Users(**user_data)
        user.save(db)
    
    # Получаем id созданных пользователей
    user_ids = [user.user_id for user in Users.get_all(db)]

    modifications = generate_modifications(50, app_ids)
    for mod_data in modifications:
        mod = Modification(**mod_data)
        mod.save(db)

    # Получаем id созданных модификаций
    mod_ids = [mod.mod_id for mod in Modification.get_all(db)]

    purchases = generate_purchases(100, user_ids, mod_ids)
    for purchase_data in purchases:
        purchase = Purchase(**purchase_data)
        purchase.save(db)

    # Получаем id созданных покупок
    purchase_ids = [purchase.purchase_id for purchase in Purchase.get_all(db)]

    checks = generate_checks(100, purchase_ids)
    for check_data in checks:
        check = Checks(**check_data)
        check.save(db)

    hwids = generate_hwids(100, user_ids)
    for hwid_data in hwids:
        hwid = HWID(**hwid_data)
        hwid.save(db)

    operations = generate_operations(100, user_ids)
    for operation_data in operations:
        operation = Operation(**operation_data)
        operation.save(db)

    subscriptions = generate_subscriptions(100, user_ids, mod_ids)
    for subscription_data in subscriptions:
        subscription = Subscription(**subscription_data)
        subscription.save(db)

    tokens = generate_tokens(100, user_ids, purchase_ids)
    for token_data in tokens:
        token = Token(**token_data)
        token.save(db)

    versions = generate_versions(100, mod_ids)
    for version_data in versions:
        version = Version(**version_data)
        version.save(db)

    db.close()

if __name__ == "__main__":
    main()