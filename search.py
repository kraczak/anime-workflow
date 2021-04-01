import sys

from db import Anime
from utils import display_anime_list, get_followed_anime, get_not_followed_anime, get_all_anime

fun_dict = {
    'followed': get_followed_anime,
    'not_followed': get_not_followed_anime,
    'all': get_all_anime
}

if __name__ == '__main__':
    args = sys.argv[1:]
    search_type = args[0]
    if len(args) == 0 or args[0] not in fun_dict:
        sys.exit(0)
    elif len(args) == 1:
        anime_list = fun_dict[search_type]()
        display_anime_list(anime_list)
    elif len(args) > 1:
        name = ' '.join(args[1:])
        anime_list = fun_dict[search_type]([Anime.name.contains(name)])
        display_anime_list(anime_list)
