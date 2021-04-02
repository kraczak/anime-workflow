from typing import List

from common import arg_sep


def parse_args(args: List[str]) -> List[str]:
    result_args = []
    for arg in args:
        if arg_sep in arg:
            new_args = [a.strip() + arg_sep for a in arg.split(arg_sep) if a != '']
            result_args.extend(new_args)
        else:
            result_args.append(arg)
    return result_args
