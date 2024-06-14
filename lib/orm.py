# Пример ORM
from enum import Enum

class FieldType(Enum):
    INT = "INT"
    SERIAL = "SERIAL"
    VARCHAR = "VARCHAR(255)"
    DATE = "DATE"
    DATETIME = "TIMESTAMP"
    DECIMAL = "DECIMAL(10,2)"

class OperationType(Enum):
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    PURCHASE = "PURCHASE"
    UPDATE_PROFILE = "UPDATE_PROFILE"

class Field:
    def __init__(self, type_, primary_key=False, foreign_key=None):
        if not isinstance(type_, FieldType):
            raise ValueError("Field type must be an instance of FieldType Enum")
        self.type = type_.value
        self.primary_key = primary_key
        self.foreign_key = foreign_key

class ModelMeta(type):
    def __init__(cls, name, bases, dct):
        if not hasattr(cls, '_registry'):
            cls._registry = {}
        else:
            cls._registry[name] = cls
        super(ModelMeta, cls).__init__(name, bases, dct)

class Model(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        for key, field in self.__class__.__dict__.items():
            if isinstance(field, Field) and key not in kwargs:
                setattr(self, key, None)

    @classmethod
    def create_table(cls, db):
        fields = []
        for attr, value in cls.__dict__.items():
            if isinstance(value, Field):
                field_def = f'{attr} {value.type}'
                if value.primary_key:
                    field_def += ' PRIMARY KEY'
                if value.foreign_key:
                    field_def += f' REFERENCES {value.foreign_key}'
                fields.append(field_def)

        query = f'CREATE TABLE IF NOT EXISTS {cls.__name__.lower()} ({", ".join(fields)});'
        with db.get_cursor() as cur:
            cur.execute(query)

    def extract_field_values(self):
        columns = []
        values = []
        for attr, field in self.__class__.__dict__.items():
            if isinstance(field, Field):
                value = getattr(self, attr)
                if value is None and field.primary_key:
                    continue
                columns.append(attr)
                values.append(value)
        return columns, values

    def save(self, db):
        columns, values = self.extract_field_values()

        if not columns:
            raise ValueError("No fields found to insert.")

        column_names = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))

        query = f'INSERT INTO {self.__class__.__name__.lower()} ({column_names}) VALUES ({placeholders}) RETURNING *;'
        with db.get_cursor() as cur:
            cur.execute(query, values)
            if self.__class__.__dict__.get(columns[0]).primary_key:
                setattr(self, columns[0], cur.fetchone()[0])

    @classmethod
    def get_all(cls, db):
        query = f'SELECT * FROM {cls.__name__.lower()};'
        with db.get_cursor() as cur:
            cur.execute(query)
            records = cur.fetchall()
            results = []
            for record in records:
                obj = cls(**dict(zip([col[0] for col in cur.description], record)))
                results.append(obj)
            return results

# Пример моделей
class Application(Model):
    app_id = Field(FieldType.SERIAL, primary_key=True)
    app_name = Field(FieldType.VARCHAR)

class Users(Model):
    user_id = Field(FieldType.SERIAL, primary_key=True)
    full_name = Field(FieldType.VARCHAR)
    email = Field(FieldType.VARCHAR)
    password = Field(FieldType.VARCHAR)
    registration_date = Field(FieldType.DATE)
    app_availability = Field(FieldType.INT, foreign_key='application(app_id)')

class Modification(Model):
    mod_id = Field(FieldType.SERIAL, primary_key=True)
    mod_name = Field(FieldType.VARCHAR)
    mod_desc = Field(FieldType.VARCHAR)
    app_id = Field(FieldType.INT, foreign_key='application(app_id)')

class Purchase(Model):
    purchase_id = Field(FieldType.SERIAL, primary_key=True)
    user_id = Field(FieldType.INT, foreign_key='users(user_id)')
    mod_id = Field(FieldType.INT, foreign_key='modification(mod_id)')
    purchase_date = Field(FieldType.DATE)

class Checks(Model):
    check_id = Field(FieldType.SERIAL, primary_key=True)
    purchase_id = Field(FieldType.INT, foreign_key='purchase(purchase_id)')
    amount = Field(FieldType.DECIMAL)
    payment_method = Field(FieldType.VARCHAR)

class HWID(Model):
    hwid_id = Field(FieldType.SERIAL, primary_key=True)
    user_id = Field(FieldType.INT, foreign_key='users(user_id)')
    processor = Field(FieldType.VARCHAR)
    videocard = Field(FieldType.VARCHAR)
    os_version = Field(FieldType.VARCHAR)
    os_type = Field(FieldType.VARCHAR)
    disks = Field(FieldType.VARCHAR)
    network_card = Field(FieldType.VARCHAR)

class Operation(Model):
    operation_id = Field(FieldType.SERIAL, primary_key=True)
    user_id = Field(FieldType.INT, foreign_key='users(user_id)')
    operation_type = Field(FieldType.VARCHAR)
    operation_date = Field(FieldType.DATETIME)

class Subscription(Model):
    subscription_id = Field(FieldType.SERIAL, primary_key=True)
    user_id = Field(FieldType.INT, foreign_key='users(user_id)')
    mod_id = Field(FieldType.INT, foreign_key='modification(mod_id)')
    subscription_time = Field(FieldType.DATETIME)

class Token(Model):
    token_id = Field(FieldType.SERIAL, primary_key=True)
    user_id = Field(FieldType.INT, foreign_key='users(user_id)')
    hwid_id = Field(FieldType.INT, foreign_key='hwid(hwid_id)')
    last_login = Field(FieldType.DATETIME)

class Version(Model):
    version_id = Field(FieldType.SERIAL, primary_key=True)
    mod_id = Field(FieldType.INT, foreign_key='modification(mod_id)')
    version_number = Field(FieldType.INT)
    version_name = Field(FieldType.VARCHAR)
    version_description = Field(FieldType.VARCHAR)
    version_link = Field(FieldType.VARCHAR)