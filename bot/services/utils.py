from time import sleep
from services.anime import anime

def test_query_schedule(day: str):
    days_of_week = [
        'monday', 'tuesday', 'wednesday',
        'thursday', 'friday', 'saturday', 'sunday']
    if day.lower() in days_of_week:
        return True
    else:
        return False

def emoji(premiered: str):
    dict_emojis = {
        'Fall': ':fallen_leaf:',
        'Spring': ':sunflower:',
        'Summer': ':sunrise:',
        'Winter': ':cloud_snow:'
    }
    emoji = [emoji for season, emoji in dict_emojis.items() if season in premiered]
    if emoji:
        return emoji[-1]
    else:
        return ''

def sort_animes(anime_found):
    flag = False
    seasons_ord = [anime_found]
    while True:
        if 'related' in anime_found and 'Prequel' in anime_found['related']:
            sleep(1)
            anime_found = anime(anime_found['related']['Prequel'][0]['mal_id'], 'seasons')
            seasons_ord.append(anime_found)
            if 'Prequel' not in anime_found['related']:
                seasons_ord.reverse()
                flag = True
                break
        else:
            break
    if flag:
        anime_found = seasons_ord[-1]
    while True:
        if 'related' in anime_found and 'Sequel' in anime_found['related']:
            sleep(1)
            anime_found = anime(anime_found['related']['Sequel'][0]['mal_id'], 'seasons')
            seasons_ord.append(anime_found)
            if 'Sequel' not in anime_found['related']:
                break
        else:
            break
    return seasons_ord