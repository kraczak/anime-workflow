import json
from typing import Dict, List

import peewee

from db import AnimeModel


def get_items_from_records(rec: List[AnimeModel]):
    return [a.to_alfred_item() for a in rec]


def get_all_anime():
    return get_items_from_records(AnimeModel.get_all())


def get_followed_anime(filters: List[peewee.Expression] = None):
    return get_items_from_records(AnimeModel.get_followed(filters))


def get_not_followed_anime(filters: List[peewee.Expression] = None):
    return get_items_from_records(AnimeModel.get_not_followed(filters))


def display_anime_list(anime_lst: List[Dict[str, str]]):
    print(json.dumps({"items": anime_lst}, ensure_ascii=False))


def create_item(title: str, subtitle: str = 'test'):
    return [{'title': title, 'subtitle': subtitle}]


def swap_following(partial_title: str):
    not_followed = AnimeModel.get_all([AnimeModel.url == partial_title])
    for a in not_followed:
        a.follow = not a.follow
        a.save()
