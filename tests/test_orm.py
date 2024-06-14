from lib.db import Database
from lib.orm import *
from lib.data_generator import *

def test_create_tables():
    db = Database(dbname='testdb')
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

def test_insert_data():
    db = Database(dbname='testdb')
    
    app = Application(app_name='TestApp')
    app.save(db)
    
    user = Users(full_name='John Doe', email='john@example.com', password='hashedpassword', registration_date='2021-01-01', app_availability=1)
    user.save(db)

    mod = Modification(mod_name='TestMod', mod_desc='Description', app_id=1)
    mod.save(db)

    purchase = Purchase(user_id=1, mod_id=1, purchase_date='2022-01-01')
    purchase.save(db)
    
    check = Checks(purchase_id=1, amount=50.00, payment_method='Credit Card')
    check.save(db)
    
    hwid = HWID(user_id=1, processor='Intel', videocard='Nvidia', os_version='Windows 10', os_type='64-bit', disks='512GB SSD', network_card='Intel')
    hwid.save(db)
    
    operation = Operation(user_id=1, operation_type=OperationType.LOGIN, operation_date='2022-02-01 10:00:00')
    operation.save(db)
    
    subscription = Subscription(user_id=1, mod_id=1, subscription_time='2022-02-01 10:00:00')
    subscription.save(db)
    
    token = Token(user_id=1, hwid_id=1, last_login='2022-02-01 10:00:00')
    token.save(db)
    
    version = Version(mod_id=1, version_number=1, version_name='v1.0', version_description='Initial version', version_link='http://example.com')
    version.save(db)

    db.close()

test_create_tables()
test_insert_data()