import operator
from functools import reduce
from typing import List

import peewee
from peewee import *

from common import db_name

db = SqliteDatabase(db_name)


class BaseModel(Model):
    class Meta:
        database = db


class Anime(BaseModel):
    name = CharField(unique=True)
    url = CharField()
    follow = BooleanField(default=True)

    def to_dict(self):
        return {'name': self.name, 'url': self.url, 'follow': self.follow}

    def to_alfred_item(self):
        return {'title': self.name, 'subtitle': self.url, 'arg': self.url}

    @staticmethod
    def get_all(filters: List[peewee.Expression] = None, op=operator.and_):
        if filters is None:
            return Anime.select().execute()
        return Anime.select().where(reduce(op, filters)).execute()

    @staticmethod
    def get_followed(filters: List[peewee.Expression] = None, op=operator.and_):
        if filters is None:
            filters = []
        tmp_filters = [Anime.follow == 1] + filters
        return Anime.select().where(reduce(op, tmp_filters)).execute()

    @staticmethod
    def get_not_followed(filters: List[peewee.Expression] = None, op=operator.and_):
        if filters is None:
            filters = []
        tmp_filters = [Anime.follow == 0] + filters
        return Anime.select().where(reduce(op, tmp_filters)).execute()

    def start_following(self):
        self.follow = True
        self.save()

    def stop_following(self):
        self.follow = False
        self.save()


def create_tables():
    with db:
        db.create_tables([Anime])
