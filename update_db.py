import os

import requests
from bs4 import BeautifulSoup

from common import db_name, base_url
from db import db, Anime, create_tables


def fetch_anime_list(url):
    anime_data = {}
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    anime_div_set = soup.find_all("div", {"class": "top-portal"})[0]
    anime_div_set = anime_div_set.find_all('a', href=True)
    for anime in anime_div_set:
        anime_name = anime.get_text().strip()
        anime_link = anime['href']
        if anime_name != 'Pozostałe serie':
            anime_data[anime_name] = anime_link
    return anime_data


if __name__ == '__main__':
    data = fetch_anime_list(base_url)

    if os.path.exists(db_name):
        os.unlink(db_name)
        create_tables()

    db_data = [{'name': name, 'url': url, 'follow': False} for name, url in data.items()]
    with db.atomic():
        Anime.insert_many(db_data).on_conflict('replace').execute()
