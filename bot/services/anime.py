import jikanpy
from time import sleep


def anime(anime_id: int, command: str):
    jikan = jikanpy.Jikan()
    sleep(1)
    try:
        anime = jikan.anime(id=anime_id)
        if anime:
            if command == 'broadcast':
                return {
                    'found': True,
                    'error': None,
                    'airing': anime['airing'],
                    'image_url': anime['image_url'],
                    'title': anime['title'],
                    'title_japanese': anime['title_japanese'],
                    'status': anime['status'],
                    'premiered': anime['premiered'],
                    'episodes': anime['episodes'],
                    'broadcast': anime['broadcast'],
                    'url': anime['url']
                }
            elif command == 'songs':
                return {
                    'found': True,
                    'error': None,
                    'title': anime['title'],
                    'title_japanese': anime['title_japanese'],
                    'image_url': anime['image_url'],
                    'op': anime['opening_themes'],
                    'end': anime['ending_themes']
                }
            elif command == 'seasons':
                return {
                    'found': True,
                    'error': None,
                    'type': anime['type'],
                    'premiered': anime['premiered'],
                    'airing': anime['airing'],
                    'image_url': anime['image_url'],
                    'title': anime['title'],
                    'title_japanese': anime['title_japanese'],
                    'status': anime['status'],
                    'episodes': anime['episodes'],
                    'url': anime['url'],
                    'related': anime['related']
                }
        else:
            return {'found': False, 'error': 'empty'}
    except jikanpy.exceptions.APIException as e:
        return {
            'found': False,
            'error': 'api_error'
        }