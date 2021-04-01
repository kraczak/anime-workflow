import sys

from utils import swap_following

if __name__ == '__main__':
    args = sys.argv[1:]
    name = args[0]
    swap_following(name)
