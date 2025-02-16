def format_time(secs):
    '''
    Format seconds as HH:MM:SS.000
    '''
    hour_str = f'{str(int(secs // 3600)).zfill(2)}'
    min_str = f'{str(int((secs % 3600) // 60)).zfill(2)}'
    sec_str = '{:06.3f}'.format(secs % 60)

    return f'{hour_str}:{min_str}:{sec_str}'


def find(d, path):
    '''
    Get the value in a nested indexible object d, reached via the provided path (list).
    '''
    value = d
    for key in path:
        try:
            value = value[key]
        except KeyError:
            return None
    return value