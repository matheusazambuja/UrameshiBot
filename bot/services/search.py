import jikanpy
from time import sleep


def search(name: str):
    jikan = jikanpy.Jikan()
    sleep(1)
    try:
        animes_researched = jikan.search(search_type='anime', query=name)
        if animes_researched:
            if animes_researched['results']:
                return {
                    'found': True,
                    'id': animes_researched['results'][0]['mal_id'],
                    'error': None
                }
        return {
            'found': False,
            'id': -1,
            'error': 'empty'
        }
    except jikanpy.exceptions.APIException as e:
        return {
            'found': False,
            'id': -1,
            'error': 'api_error'
        }
