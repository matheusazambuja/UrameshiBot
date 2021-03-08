import jikanpy
from time import sleep
from services import utils

def schedule(day: str):
    try:
        if utils.validate_day_week(day):
            jikan = jikanpy.Jikan()
            sleep(1)

            animes_today = jikan.schedule(day=day)
            if animes_today[day]:
                return {
                    'found': True,
                    'error': None,
                    'results': animes_today[day]
                }
            else:
                return {
                    'found': False,
                    'error': 'empty'
                }
        else:
            return {
                'found': False,
                'error': 'parameter_error'
            }
    except jikanpy.exceptions.APIException as e:
        return {
            'found': False,
            'error': 'api_error'
        }