

def even_evens(some_list):
    """
    Give a list 'some_list', return a list of only the even numbers from the
    even indices of 'some_list'.

    """
    return [x for x in some_list[::2] if x % 2 == 0]


