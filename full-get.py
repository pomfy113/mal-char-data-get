"""Main function."""

import urllib.request
import json
import sys
from html import unescape
import time
import datetime
import pickle
import os


def API_call(MAL_id):
    """
    Receive data from API.

    Calls jikan.moe instead of the official MAL API for ease of use.
    May change this later on? For the time being, Jikan is the best tool.
    """
    time.sleep(0.2)
    API_url = "http://api.jikan.moe/anime/{}/characters_staff".format(MAL_id)

    # Error checking
    try:
        data = urllib.request.urlopen(API_url)
    except urllib.error.URLError as e:
        print(e)
        return None

    result = json.loads(data.read())

    return result

def get_themes(title, data):
    themes = []
    for op in data['opening_theme']:
        opening = "{},opening,{}\n".format(title, op)
        themes.append(opening)
    for ed in data['ending_theme']:
        ending = "{},ending,{}\n".format(title, ed)
        themes.append(ending)
    return themes

def get_cast(title, data):
    cast = []
    for char in data['character']:
        role = char['role']
        name = unescape(char['name'])
        if(char['voice_actor']):
            seiyuu = unescape(char['voice_actor'][0]['name'])
        else:
            seiyuu = "N/A"

        # Cleaned up array for writing into csv
        row = "{},\"{}\",{},\"{}\"\n".format(title, name, role, seiyuu)
        cast.append(row)
        # Insert line into csv
    return cast

def ID_get(file):
    """Grabs all MAL IDs from a text file."""
    inputfile = open(file).read()
    return inputfile.split("\n")[:-1]

def updateCheck():
    if os.path.exists('auto.p'):
        return pickle.load( open( "auto.p", "rb" ) )
    else:
        print("Previous data not found.")
        return {}

def write(data, target):
    for item in data:
        target.write(item)

def write_to_csv(id_arr, cast_target, theme_target):
    """Perform an API call per ID and write onto a csv."""
    total = len(id_arr)
    data = []
    progress = 0
    error = []

    prevData = updateCheck()

    for index, id in enumerate(id_arr):
        # Let's give the API a break
        time.sleep(10)

        result = API_call(id)

        # In case of issues involving timing, retry with a delay
        if result is None:
            print("Error - did not get id: {}. Retrying;".format(id))
            time.sleep(10)
            result = API_call(id)

        if result:
            title_eng = result['title_english']
            title = title_eng if title_eng else result['title']

            if (id in prevData) and (result == prevData[id][0]):
                print("Data is similar. Using saved data.")
                themes = prevData[id][1]
                cast = prevData[id][2]
            else:
                print("No similar data found - adding")
                themes = get_themes(title, result)
                cast = get_cast(title, result)

                prevData[id] = (result, themes, cast)

            write(themes, theme_target)
            write(cast, cast_target)
            print("Complete. {} out of {}.\n".format(index + 1, total))
        else:
            print("Could not get data.\n")
            error.append(id)

    if len(error) > 0:
        errors = open('./input/errors.txt'.format(time), 'w')
        errors.write(error)
        print("Could not get IDs: {}".format(error))

    pickle.dump(prevData, open( "auto.p", "wb" ))



def main():
    """Perform main function."""
    if len(sys.argv) != 2:
        print("Usage: python create-csv.py [file with ID input]")
        return None

    print("Script beginning - pulling IDs")

    time = datetime.datetime.now().isoformat()

    id_arr = ID_get('./input/{}'.format(sys.argv[1]))           # ID Read target
    target = open('./output/season-{}.csv'.format(time), 'w')       # Data Write target
    theme_target = open('./output/op-ed-{}.csv'.format(time), 'w')  # OP write target

    write_to_csv(id_arr, target, theme_target)

    print("Script complete. See '{}.csv' for results".format(time))

    return


if __name__ == "__main__":
    main()
