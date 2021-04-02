#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys
from datetime import datetime, timedelta
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from db import AnimeModel
from utils import get_followed_anime, display_anime_list


def parse_recent_episode(ep_tag, anime_main_page):
    td_list = ep_tag.find_all('td')
    ep_info = td_list[0].find('a', href=True)
    link = urljoin(anime_main_page, ep_info['href'])
    ep_name = ep_info.get_text()
    date = datetime.fromtimestamp(int(td_list[1].attrs['rel']))
    curr_date = datetime.now()
    state = "nadchodzi" if curr_date <= date else "zakończony"
    return ep_name, {'link': link.lower(), 'state': state, 'date': date}


def get_info_about_anime(anime_webpage):
    data = {}
    response = requests.get(anime_webpage)
    soup = BeautifulSoup(response.text, 'lxml')
    series_table_set = soup.find('table', {'class': 'lista'})
    episodes_list = series_table_set.find_all('tr')

    for ep in episodes_list:
        name, ep_data = parse_recent_episode(ep, anime_webpage)
        data[name] = ep_data
    return data


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) == 1:
        a_name = args[0]
        tmp_name = a_name.lower()

        anime_data = get_followed_anime([AnimeModel.url.contains(tmp_name)])
        if len(anime_data) > 1:
            display_anime_list(anime_data)
        else:
            data = get_info_about_anime(anime_data[0]['arg'])
            print(
                json.dumps(
                    {
                        "items": [
                            {
                                "title": name,
                                "subtitle": f"{value['state']} - {value['date']}",
                                "arg": value['link'].lower()
                            } for name, value in data.items()
                        ]
                    },
                    ensure_ascii=False)
            )
