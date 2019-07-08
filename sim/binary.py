def count_ones(value: int) -> int:
    return "{:08b}".format(value).count('1')


def count_zeros(value: int) -> int:
    return "{:08b}".format(value).count('0')
