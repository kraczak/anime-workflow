import json
import sys

from anime import get_info_about_anime
from arg_parser import parse_args
from common import arg_sep
from db import AnimeModel
from utils import display_anime_list, get_followed_anime, get_not_followed_anime, get_all_anime

fun_dict = {
    'followed': get_followed_anime,
    'not_followed': get_not_followed_anime,
    'all': get_all_anime
}

if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    search_type = args[0]
    if len(args) == 0 or args[0] not in fun_dict:
        sys.exit(0)
    elif len(args) == 1:
        anime_list = fun_dict[search_type]()
        display_anime_list(anime_list)
    elif len(args) > 1:
        tmp_name = ' '.join(args[1:])
        name = tmp_name
        if name.endswith(arg_sep):
            name = name[:-1]

        anime_list = fun_dict[search_type]([AnimeModel.name.contains(name)])

        if '▹' in tmp_name and len(anime_list) == 1:
            data = get_info_about_anime(anime_list[0]['arg'])
            print(
                json.dumps(
                    {
                        "items": [
                            {
                                "title": name,
                                "subtitle": f"{value['state']} - {value['date']}",
                                "arg": value['link'].lower(),
                                "autocomplete": f'{tmp_name} {name}',
                            } for name, value in data.items()
                        ]
                    },
                    ensure_ascii=False)
            )
        else:
            display_anime_list(anime_list)
