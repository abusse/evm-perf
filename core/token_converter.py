from core.tokens import *

converter_functions = {'RAND': rand,
                       'MINIT': minit}


def convert_token(token_string: str) -> str:
    t = token_string.split(',')
    token = t[0].upper()
    token_args = t[1:]

    if token not in converter_functions:
        raise NameError(f'Cannot find {token}')

    return converter_functions[token](token_args)
