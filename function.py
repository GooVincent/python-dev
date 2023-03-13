""" Testing
    positional-only arguments passed as keyword arguments
"""


def fun_position_args(a, b, /, c, d):
    return a+b+c+d


def fun_keyword_args(a, b, *, c, d):
    return a+b+c+d


if __name__ == '__main__':
    # fun_position_args(1, b=2, c=3, d=4) # bad case
    fun_position_args(1, b=2, c=3, d=4)

    # fun_keyword_args(1, b=2, 3, 4)  # bad case
    fun_keyword_args(1, 2, c=3, d=4)


