from typing import List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag
from pydantic import BaseModel

from anime import parse_recent_episode
from table_parser import TableParser


class AlfredItem(BaseModel):
    title: str
    subtitle: str
    arg: str
    autocomplete: str
    valid: bool


class Anime(BaseModel):
    name: str
    source: str
    date: str
    url: str


class Series(BaseModel):
    name: str
    url: str

    def to_alfred_record(self):
        return {'title': self.name, 'subtitle': self.url, 'arg': self.url}


class Episode(BaseModel):
    name: str
    source: str
    date: str
    url: str


class Player(BaseModel):
    lan: str


def parse_row(row: Tag, columns: List[str], column_tag: str, href: int, skip_col: List[int]):
    kwargs = {}
    for i, col_value in enumerate(row.find_all(column_tag)):
        if href == i:
            kwargs['url'] = col_value.find('a', href=True)['href']
        if i not in skip_col:
            kwargs[columns[i]] = col_value.get_text()
    return kwargs


def parse_player_row(row: Tag, columns: List[str], column_tag: str, href: int, skip_col: List[int]):
    kwargs = {}
    for i, col_value in enumerate(row.find_all(column_tag)):
        if href == i:
            url = col_value.find('span')['rel']
            kwargs['url'] = f'odtwarzacz-{url}.html'
        if i not in skip_col:
            kwargs[columns[i]] = col_value.get_text()
    return kwargs


def parse_table(
        table: Tag,
        columns: List[str],
        row_tag: str,
        column_tag: str,
        href: int,
        output_class=None,
        skip_row=-1,
        skip_col=None
):
    row_list = table.find_all(row_tag)
    result = []
    skip_col = skip_col or []
    for i, row in enumerate(row_list):
        if i != skip_row:
            kwargs = parse_row(row, columns, column_tag, href, skip_col)
            if output_class is not None:
                result.append(output_class(**kwargs))
            else:
                result.append(kwargs)
    return result


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
        table_parser = TableParser()
        table_parser.parse(table, [0])
        ep_list = parse_table(table, ['name', 'source', 'date'], 'tr', 'td', 0, Episode)
        for e in ep_list:
            e.url = urljoin(series_url, e.url)
        return ep_list

    @staticmethod
    def fetch_players_for_episode(episode_url: str):
        response = requests.get(episode_url)
        sp = BeautifulSoup(response.text, 'lxml')
        table = sp.find('table')
        return parse_table(table, ['a', 'b', 'name', 'source', 'link'], 'tr', 'td', 4, skip_row=0)


if __name__ == '__main__':
    ap = AnimeParser()
    base_url = 'https://wbijam.pl'
    anime_list = ap.fetch_anime_list(base_url)

    for anime_url in anime_list.values():

        series = ap.fetch_anime_series('https://blackclover.wbijam.pl/pierwsza_seria.html')
        for s in series:
            for ep in ap.fetch_episodes_from_series(s.url):
                ap.fetch_players_for_episode(ep.url)
            break
        break
