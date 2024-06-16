import sys
import os

# Добавляем путь к родительской директории для корректного импорта модулей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from datetime import datetime
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

DATABASE_NAME = 'test_db'  # имя тестовой базы данных для тестов

@pytest.fixture(scope='module')
def db():
    test_db = Database(DATABASE_NAME)
    test_db._ensure_database()

    with test_db as connection:
        yield connection

    test_db.drop_db(DATABASE_NAME)

@pytest.fixture(autouse=True)
def setup_and_teardown(db):
    # Создание таблиц перед каждым тестом
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

    Users.create_many_to_many_tables(db)

    yield
    
    # Удаление данных в правильной последовательности для избежания ошибкок внешнего ключа
    tables = ['checks', 'purchase', 'subscription', 'token', 'operation', 'hwid', 'version', 'users_modification', 'modification', 'users', 'application']
    for table in tables:
        db.delete_all_data(table)

def test_application_insert(db):
    app = Application(app_name="Test Application")
    app.save(db)

    apps = Application.get_all(db)
    assert len(apps) == 1
    assert apps[0].app_name == "Test Application"

def test_users_insert(db):
    app = Application(app_name="Test Application")
    app.save(db)
    app_id = app.app_id

    user = Users(
        full_name="John Doe",
        email="john.doe@example.com",
        password="password",
        registration_date=datetime.now().date(),
        app_availability=app_id
    )
    user.save(db)

    users = Users.get_all(db)
    assert len(users) == 1
    assert users[0].full_name == "John Doe"

def test_modification_insert(db):
    app = Application(app_name="Test Application")
    app.save(db)
    app_id = app.app_id

    mod = Modification(
        mod_name="Test Modification",
        mod_desc="A test modification.",
        app_id=app_id
    )
    mod.save(db)

    mods = Modification.get_all(db)
    assert len(mods) == 1
    assert mods[0].mod_name == "Test Modification"

def test_purchase_insert(db):
    app = Application(app_name="Test Application")
    app.save(db)
    app_id = app.app_id

    user = Users(
        full_name="John Doe",
        email="john.doe@example.com",
        password="password",
        registration_date=datetime.now().date(),
        app_availability=app_id
    )
    user.save(db)
    user_id = user.user_id

    mod = Modification(
        mod_name="Test Modification",
        mod_desc="A test modification.",
        app_id=app_id
    )
    mod.save(db)
    mod_id = mod.mod_id

    purchase = Purchase(
        user_id=user_id,
        mod_id=mod_id,
        purchase_date=datetime.now().date()
    )
    purchase.save(db)

    purchases = Purchase.get_all(db)
    assert len(purchases) == 1
    assert purchases[0].user_id == user_id

def test_checks_insert(db):
    app = Application(app_name="Test Application")
    app.save(db)
    app_id = app.app_id

    user = Users(
        full_name="John Doe",
        email="john.doe@example.com",
        password="password",
        registration_date=datetime.now().date(),
        app_availability=app_id
    )
    user.save(db)
    user_id = user.user_id

    mod = Modification(
        mod_name="Test Modification",
        mod_desc="A test modification.",
        app_id=app_id
    )
    mod.save(db)
    mod_id = mod.mod_id

    purchase = Purchase(
        user_id=user_id,
        mod_id=mod_id,
        purchase_date=datetime.now().date()
    )
    purchase.save(db)
    purchase_id = purchase.purchase_id

    checks = Checks(
        purchase_id=purchase_id,
        amount=99.99,
        payment_method="Credit Card"
    )
    checks.save(db)

    all_checks = Checks.get_all(db)
    assert len(all_checks) == 1
    assert float(all_checks[0].amount) == 99.99

def test_hwid_insert(db):
    app = Application(app_name="Test Application")
    app.save(db)
    app_id = app.app_id

    user = Users(
        full_name="John Doe",
        email="john.doe@example.com",
        password="password",
        registration_date=datetime.now().date(),
        app_availability=app_id
    )
    user.save(db)
    user_id = user.user_id

    hwid = HWID(
        user_id=user_id,
        processor="Intel",
        videocard="NVIDIA",
        os_version="Windows 10",
        os_type="64-bit",
        disks="1TB SSD",
        network_card="Intel Ethernet"
    )
    hwid.save(db)

    hwids = HWID.get_all(db)
    assert len(hwids) == 1
    assert hwids[0].processor == "Intel"

def test_operation_insert(db):
    app = Application(app_name="Test Application")
    app.save(db)
    app_id = app.app_id

    user = Users(
        full_name="John Doe",
        email="john.doe@example.com",
        password="password",
        registration_date=datetime.now().date(),
        app_availability=app_id
    )
    user.save(db)
    user_id = user.user_id

    operation = Operation(
        user_id=user_id,
        operation_type="LOGIN",
        operation_date=datetime.now()
    )
    operation.save(db)

    operations = Operation.get_all(db)
    assert len(operations) == 1
    assert operations[0].operation_type == "LOGIN"

def test_subscription_insert(db):
    app = Application(app_name="Test Application")
    app.save(db)
    app_id = app.app_id

    user = Users(
        full_name="John Doe",
        email="john.doe@example.com",
        password="password",
        registration_date=datetime.now().date(),
        app_availability=app_id
    )
    user.save(db)
    user_id = user.user_id

    mod = Modification(
        mod_name="Test Modification",
        mod_desc="A test modification.",
        app_id=app_id
    )
    mod.save(db)
    mod_id = mod.mod_id

    subscription = Subscription(
        user_id=user_id,
        mod_id=mod_id,
        subscription_time=datetime.now()
    )
    subscription.save(db)

    subscriptions = Subscription.get_all(db)
    assert len(subscriptions) == 1
    assert subscriptions[0].user_id == user_id

def test_token_insert(db):
    app = Application(app_name="Test Application")
    app.save(db)
    app_id = app.app_id

    user = Users(
        full_name="John Doe",
        email="john.doe@example.com",
        password="password",
        registration_date=datetime.now().date(),
        app_availability=app_id
    )
    user.save(db)
    user_id = user.user_id

    hwid = HWID(
        user_id=user_id,
        processor="Intel",
        videocard="NVIDIA",
        os_version="Windows 10",
        os_type="64-bit",
        disks="1TB SSD",
        network_card="Intel Ethernet"
    )
    hwid.save(db)
    hwid_id = hwid.hwid_id

    token = Token(
        user_id=user_id,
        hwid_id=hwid_id,
        last_login=datetime.now()
    )
    token.save(db)

    tokens = Token.get_all(db)
    assert len(tokens) == 1
    assert tokens[0].user_id == user.user_id

def test_version_insert(db):
    app = Application(app_name="Test Application")
    app.save(db)
    app_id = app.app_id

    mod = Modification(
        mod_name="Test Modification",
        mod_desc="A test modification.",
        app_id=app_id
    )
    mod.save(db)
    mod_id = mod.mod_id

    version = Version(
        mod_id=mod_id,
        version_number=1,
        version_name="v1.0",
        version_description="Initial Release",
        version_link="http://example.com/download"
    )
    version.save(db)

    versions = Version.get_all(db)
    assert len(versions) == 1
    assert versions[0].version_name == "v1.0"

def test_many_to_many_insert(db):
    app = Application(app_name="Test Application")
    app.save(db)
    app_id = app.app_id

    mod = Modification(
        mod_id = "666",
        mod_name="Test Modification",
        mod_desc="A test modification.",
        app_id=app_id
    )
    mod.save(db)
    print(Modification.get_all(db))
    mod_id = Modification.get_all(db)[0].mod_id

    user = Users(
        user_id="666",
        full_name="John Doe",
        email="john.doe@example.com",
        password="password",
        registration_date=datetime.now().date(),
        app_availability=app_id
    )
    user.save(db)
    user_id = Users.get_all(db)[0].user_id
    
    with db.get_cursor() as cursor:
        cursor.execute(
            f"INSERT INTO users_modification (user_id, mod_id) VALUES ({user_id}, {mod_id})"
        )
    
    with db.get_cursor() as cursor:
        cursor.execute("SELECT * FROM users_modification")
        mm_records = cursor.fetchall()
        assert len(mm_records) == 1
        assert mm_records[0][0] == user_id
        assert mm_records[0][1] == mod_id

def test_generate_data(db):
    apps = list(generate_application_data(1))
    for app in apps:
        app.save(db)
    app_ids = [app.app_id for app in Application.get_all(db)]

    users = list(generate_user_data(1, app_ids))
    for user in users:
        user.app_availability = app_ids[0]
        user.save(db)
    user_ids = [user.user_id for user in Users.get_all(db)]

    mods = list(generate_modification_data(1, app_ids))
    for mod in mods:
        mod.save(db)
    mod_ids = [mod.mod_id for mod in Modification.get_all(db)]

    purchases = list(generate_purchase_data(1, user_ids, mod_ids))
    for purchase in purchases:
        purchase.save(db)
    purchase_ids = [purchase.purchase_id for purchase in Purchase.get_all(db)]

    checks = list(generate_check_data(1, purchase_ids))
    for chk in checks:
        chk.save(db)

    hwids = list(generate_hwid_data(1, user_ids))
    for hw in hwids:
        hw.save(db)
    hwid_ids = [hw.hwid_id for hw in HWID.get_all(db)]

    operations = list(generate_operation_data(1, user_ids))
    for operation in operations:
        operation.save(db)

    subscriptions = list(generate_subscription_data(1, user_ids, mod_ids))
    for subscription in subscriptions:
        subscription.save(db)
    
    tokens = list(generate_token_data(1, user_ids, hwid_ids))
    for token in tokens:
        token.save(db)

    versions = list(generate_version_data(1, mod_ids))
    for version in versions:
        version.save(db)

    assert len(Application.get_all(db)) == 1
    assert len(Users.get_all(db)) == 1
    assert len(Modification.get_all(db)) == 1
    assert len(Purchase.get_all(db)) == 1
    assert len(Checks.get_all(db)) == 1
    assert len(HWID.get_all(db)) == 1
    assert len(Operation.get_all(db)) == 1
    assert len(Subscription.get_all(db)) == 1
    assert len(Token.get_all(db)) == 1
    assert len(Version.get_all(db)) == 1