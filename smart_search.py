def is_sub_sequence(a, b):
    """ search if a is a subsequence of b """
    i, j = 0, 0
    max_string = len(a)
    max_search = len(b)
    if max_search > max_string:
        return False
    while j < max_search:
        while i < max_string:
            if a[i] == b[j]:
                j += 1
            i += 1
            if j == max_search:
                return True
        return False
