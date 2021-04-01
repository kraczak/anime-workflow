#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from db import Anime
from utils import get_all_anime, get_followed_anime, display_anime_list


def parse_episode(ep_tag, anime_main_page):
    """
    </tr>
    <tr class="lista_hover" rel="">
    <td><img alt="" src="images/tv_info.gif"/> <a class="sub_inner_link" href="boruto-190.html">Boruto 190: "Ucieczka"</a></td>
    <td class="lista_td_calendar" rel="1615710600">00 dni 00:00:00</td>
    <td class="lista_td">14.03.2021</td>
    </tr>
    """
    td_list = ep_tag.find_all('td')
    ep_info = td_list[0].find('a', href=True)
    link = urljoin(anime_main_page, ep_info['href'])
    ep_name = ep_info.get_text()
    state = td_list[1].get_text()
    if ep_tag.attrs['rel'] != '':
        state = ep_tag.attrs['rel'].lower()
    elif state == '00 dni 00:00:00':
        state = "zakończony"
    date = td_list[2].get_text()
    return ep_name, {'link': link.lower(), 'state': state, 'date': date}


def get_info_about_anime(anime_webpage):
    # print(anime_webpage)
    data = {}
    response = requests.get(anime_webpage)
    soup = BeautifulSoup(response.text, 'lxml')
    series_table_set = soup.find('table', {'class': 'lista'})
    episodes_list = series_table_set.find_all('tr')

    for ep in episodes_list:
        name, ep_data = parse_episode(ep, anime_webpage)
        data[name] = ep_data
    return data


args = sys.argv[1:]
try:
    anime_data = get_all_anime()
    if len(args) == 0:
        print(json.dumps({'items': anime_data}, ensure_ascii=False))
        pass
    else:
        a_name = args[0]
        tmp_name = a_name.lower()

        anime_data = get_followed_anime([Anime.url.contains(tmp_name)])
        display_anime_list(anime_data)
        # data = get_info_about_anime(anime_data[key])
        # print(
        #     json.dumps(
        #         {
        #             "items": [
        #                 {
        #                     "title": name,
        #                     "subtitle": f"{value['state']} - {value['date']}",
        #                     "arg": value['link'].lower()
        #                 } for name, value in data.items()
        #             ]
        #         },
        #         ensure_ascii=False)
        # )
except Exception as err:
    raise err
