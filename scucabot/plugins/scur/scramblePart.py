from .data_source import scramble_url
from .utils import response

def scramble_display(event: str):
    msg = get_scramble(event)
    return msg

def get_scramble(event: str):
    url = f'{scramble_url}{event}'
    scramble = response(url)['scrambles']
    return scramble