import os

from anime_parser import AnimeParser
from common import db_name, base_url
from db import db, AnimeModel, create_tables

if __name__ == '__main__':
    data = AnimeParser().fetch_anime_list(base_url)

    if os.path.exists(db_name):
        os.unlink(db_name)
        create_tables()

    db_data = [{'name': name, 'url': url, 'follow': False} for name, url in data.items()]
    with db.atomic():
        AnimeModel.insert_many(db_data).on_conflict('replace').execute()
