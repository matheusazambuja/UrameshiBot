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

def _radix_sort_msd(lista, i):
    if len(lista) <= 1:
        return lista
    else:
        lista_ordenada = []
        lista_aux = [[] for x in range(36)]  # 37: um espaço para cada letra do alfabeto e numeros

        for s in lista:
            if i >= len(s):
                lista_ordenada.append(s)
            else:
                if s[i].isdigit():
                    lista_aux[ord(s[i]) - 48].append(s)
                else:
                    lista_aux[ord(s[i].upper()) - ord('A') + 10].append(s)

        lista_aux = [_radix_sort_msd(b, i + 1) for b in lista_aux]

        return lista_ordenada + [b for blist in lista_aux for b in blist]

def _clear_string(string, alphabet):
    i = 0
    cleaned_string = string
    while i < len(cleaned_string):
        if cleaned_string[i].upper() not in alphabet:
            cleaned_string = cleaned_string.replace(cleaned_string[i], '')
        else:
            i += 1
    return cleaned_string

def sort_animes(list_animes, query):
    alphabet = [chr(c) for c in range(48, 58)] + [chr(c) for c in range(65, 91)]
    nameclean_and_anime = [[_clear_string(a['title'], alphabet), a] for a in list_animes]

    animes = []
    query = _clear_string(query, alphabet).upper()
    for element in nameclean_and_anime:
        dif = False
        i, j = 0, 0
        index = min(len(query), len(element[0]))
        element[0] = element[0].upper()
        while i < len(query) and j < len(element[0]):
            if query[i] != element[0][j]:
                if element[0][j-1] != element[0][j]:
                    dif = True
                    break
                else:
                    j += 1
            else:
                j += 1
                i += 1
        if not dif and i >= len(query):
            animes.append(element)
    animes_sorted = []
    names_sort = _radix_sort_msd([a[0] for a in animes], 0)
    for i, n in enumerate(names_sort):
        for a in animes:
            if n == a[0]:
                animes_sorted.append(a[-1])
                break

    return animes_sorted