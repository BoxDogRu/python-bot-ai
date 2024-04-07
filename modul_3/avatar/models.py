from datetime import datetime
from playhouse.postgres_ext import *
from playhouse.shortcuts import model_to_dict

import logging
import os
from dotenv import load_dotenv

from models_init import init_methods, init_models

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')

db = PostgresqlExtDatabase(
    DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST
)


class User(Model):
    telegram_id = IntegerField(unique=True, index=True) # telegram_id
    created_at = DateTimeTZField(default=datetime.now)
    updated_at = DateTimeTZField(default=datetime.now)
    username = CharField(default="")
    first_name = CharField(default="")
    last_name = CharField(default="")
    language_code = CharField(default="")
    deep_link = CharField(default="")
    is_premium = BooleanField(default=False, index=True)
    is_admin = BooleanField(default=False, index=True)

    class Meta:
        database = db
        db_table = "user"

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super(User, self).save(*args, **kwargs)

    def delete_user(self):
        self.delete_instance()

    def get_user_data_dict(self):
        user_data_dict = model_to_dict(self)
        for k, v in user_data_dict.items():
            if isinstance(v, datetime):
                user_data_dict[k] = v.isoformat()  # convert datetime to a string
        return user_data_dict

    def get_user_data_json(self):
        user_data_dict = self.get_user_data_dict()
        return json.dumps(user_data_dict)

    @classmethod
    def get_all_users(cls):
        query = cls.select()
        return [model_to_dict(user) for user in query]


class GPTModel(Model):
    model_id = CharField(default="model_id", unique=True)
    name = CharField(default="Название модели")

    class Meta:
        database = db
        db_table = "gpt_model"


class GPTMethod(Model):
    method = CharField(default="Задача", unique=True)
    url = CharField(default="https://")

    class Meta:
        database = db
        db_table = "gpt_method"


class GPTModelSET(Model):
    id = AutoField()
    modelUri = CharField()
    stream = BooleanField(default=False)
    temperature = FloatField(default=0.5)
    max_tokens = IntegerField(default=2000)

    class Meta:
        database = db
        db_table = "gpt_model_set"


class GPTRequest(Model):
    user = ForeignKeyField(User, backref='gpt_model')
    gpt_model = ForeignKeyField(GPTModel, backref='model')
    gpt_method = ForeignKeyField(GPTMethod, backref='gpt_method')
    gpt_model_set = ForeignKeyField(GPTModelSET, backref='gpt_model_set')
    request_body = JSONField()
    response = JSONField()

    class Meta:
        database = db
        db_table = "gpt_request"


db.connect()
if not User.table_exists():
    db.create_tables([User])
if not GPTModel.table_exists():
    db.create_tables([GPTModel])
    for model_id, name in init_models.items():
        GPTModel.create(model_id=model_id, name=name)
if not GPTMethod.table_exists():
    db.create_tables([GPTMethod])
    for task, url in init_methods.items():
        GPTMethod.create(method=task, url=url)
if not GPTModelSET.table_exists():
    db.create_tables([GPTModelSET])
if not GPTRequest.table_exists():
    db.create_tables([GPTRequest])