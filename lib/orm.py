import re
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
    def __new__(cls, name, bases, dct):
        docstring = dct.get('__doc__')
        if docstring:
            field_definitions = re.findall(r'(\w+): FieldType\.(\w+)(, primary_key=True)?(, foreign_key=\'(.+?)\')?', docstring)
            for field_name, field_type, primary_key, _, foreign_key in field_definitions:
                primary_key = bool(primary_key)
                field_type_enum = FieldType[field_type]
                dct[field_name] = Field(field_type_enum, primary_key, foreign_key)
        return super().__new__(cls, name, bases, dct)

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
                if isinstance(value, Enum):
                    value = value.value
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
    """
    app_id: FieldType.SERIAL, primary_key=True
    app_name: FieldType.VARCHAR
    """

class Users(Model):
    """
    user_id: FieldType.SERIAL, primary_key=True
    full_name: FieldType.VARCHAR
    email: FieldType.VARCHAR
    password: FieldType.VARCHAR
    registration_date: FieldType.DATE
    app_availability: FieldType.INT, foreign_key='application(app_id)'
    """

class Modification(Model):
    """
    mod_id: FieldType.SERIAL, primary_key=True
    mod_name: FieldType.VARCHAR
    mod_desc: FieldType.VARCHAR
    app_id: FieldType.INT, foreign_key='application(app_id)'
    """

class Purchase(Model):
    """
    purchase_id: FieldType.SERIAL, primary_key=True
    user_id: FieldType.INT, foreign_key='users(user_id)'
    mod_id: FieldType.INT, foreign_key='modification(mod_id)'
    purchase_date: FieldType.DATE
    """

class Checks(Model):
    """
    check_id: FieldType.SERIAL, primary_key=True
    purchase_id: FieldType.INT, foreign_key='purchase(purchase_id)'
    amount: FieldType.DECIMAL
    payment_method: FieldType.VARCHAR
    """

class HWID(Model):
    """
    hwid_id: FieldType.SERIAL, primary_key=True
    user_id: FieldType.INT, foreign_key='users(user_id)'
    processor: FieldType.VARCHAR
    videocard: FieldType.VARCHAR
    os_version: FieldType.VARCHAR
    os_type: FieldType.VARCHAR
    disks: FieldType.VARCHAR
    network_card: FieldType.VARCHAR
    """

class Operation(Model):
    """
    operation_id: FieldType.SERIAL, primary_key=True
    user_id: FieldType.INT, foreign_key='users(user_id)'
    operation_type: FieldType.VARCHAR
    operation_date: FieldType.DATETIME
    """

class Subscription(Model):
    """
    subscription_id: FieldType.SERIAL, primary_key=True
    user_id: FieldType.INT, foreign_key='users(user_id)'
    mod_id: FieldType.INT, foreign_key='modification(mod_id)'
    subscription_time: FieldType.DATETIME
    """

class Token(Model):
    """
    token_id: FieldType.SERIAL, primary_key=True
    user_id: FieldType.INT, foreign_key='users(user_id)'
    hwid_id: FieldType.INT, foreign_key='hwid(hwid_id)'
    last_login: FieldType.DATETIME
    """

class Version(Model):
    """
    version_id: FieldType.SERIAL, primary_key=True
    mod_id: FieldType.INT, foreign_key='modification(mod_id)'
    version_number: FieldType.INT
    version_name: FieldType.VARCHAR
    version_description: FieldType.VARCHAR
    version_link: FieldType.VARCHAR
    """