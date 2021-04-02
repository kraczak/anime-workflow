from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from anime import parse_recent_episode
from models import Series, Episode, Player
from table_parser import TableParser


class AnimeParser:
    @staticmethod
    def fetch_anime_list(website: str):
        anime_data = {}
        response = requests.get(website)
        soup = BeautifulSoup(response.text, 'lxml')
        anime_div_set = soup.find_all("div", {"class": "top-portal"})[0]
        anime_div_set = anime_div_set.find_all('a', href=True)
        for anime in anime_div_set:
            anime_name = anime.get_text().strip()
            anime_link = anime['href']
            if anime_name != 'Pozostałe serie':
                anime_data[anime_name] = anime_link
        return anime_data

    @staticmethod
    def fetch_recent_anime_episodes(anime_website: str):
        data = {}
        response = requests.get(anime_website)
        soup = BeautifulSoup(response.text, 'lxml')
        series_table_set = soup.find('table', {'class': 'lista'})
        episodes_list = series_table_set.find_all('tr')

        for ep in episodes_list:
            name, ep_data = parse_recent_episode(ep, anime_website)
            data[name] = ep_data
        return data

    @staticmethod
    def fetch_anime_series(anime_website: str):
        response = requests.get(anime_website)
        soup = BeautifulSoup(response.text, 'lxml')
        series_list = [x for x in soup.find_all('ul', {'class': 'pmenu'})][1].find_all('a', href=True)
        result = []
        for s in series_list:
            name = s.get_text()
            if "kolejność" not in name.lower():
                url = urljoin(anime_website, s['href'])
                result.append(Series(name=name, url=url))
        return result

    @staticmethod
    def fetch_episodes_from_series(series_url: str):
        response = requests.get(series_url)
        sp = BeautifulSoup(response.text, 'lxml')
        table = sp.find('table')
        ep_list = TableParser().parse(table, Episode, ['name', 'source', 'date'], [0], base_url=series_url)
        return ep_list

    @staticmethod
    def fetch_players_for_episode(episode_url: str):
        response = requests.get(episode_url)
        sp = BeautifulSoup(response.text, 'lxml')
        table = sp.find('table')
        pl_list = TableParser().parse(
            table, Player, ['server', 'link', 'url'],
            href=[4],
            href_getter=lambda col_value: f"odtwarzacz-{col_value.find('span')['rel']}.html",
            skip_rows=[0],
            skip_cols=[0, 1, 3],
            base_url=episode_url
        )
        return pl_list
