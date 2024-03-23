from datetime import datetime
from playhouse.postgres_ext import *
from playhouse.shortcuts import model_to_dict

import logging
import os
from dotenv import load_dotenv

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


class APIRequest(Model):
    request_body = JSONField()
    response = JSONField()

    class Meta:
        database = db
        db_table = "gpt_request"


db.connect()
if not User.table_exists():
    db.create_tables([User])
if not APIRequest.table_exists():
    db.create_tables([APIRequest])
