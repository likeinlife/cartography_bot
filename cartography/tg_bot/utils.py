def make_float_list_from_str(data: str):
    return list(map(float, data.strip(' ').split(' ')))
