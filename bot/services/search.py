import jikanpy
from time import sleep
from services import utils


def search(name: str):
    jikan = jikanpy.Jikan()
    sleep(1)
    try:
        animes_researched = jikan.search(search_type='anime', query=name)
        if animes_researched:
            if animes_researched['results']:
                results = utils.sort_animes(animes_researched['results'], query=name)
                if results:
                    return {
                        'found': True,
                        'id': results[0]['mal_id'],
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
