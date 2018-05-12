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
        return None

    result = json.loads(data.read())

    return result

def get_themes(title, data, target, write=False):
    themes = []
    for op in data['opening_theme']:
        opening = "{},opening,{}\n".format(title, op)
        if write is True:
            target.write(opening)
        else:
            themes.append(opening)
    for ed in data['ending_theme']:
        ending = "{},ending,{}\n".format(title, ed)
        if write is True:
            target.write(ending)
        else:
            themes.append(ending)
    return themes

def get_cast(title, data, target, write=False):
    cast = []
    for char in data['character']:
        role = char['role']
        name = unescape(char['name'])
        if(char['voice_actor']):
            seiyuu = unescape(char['voice_actor'][0]['name'])
        else:
            seiyuu = "N/A"

        # Cleaned up array for writing into csv
        row = "{},{},{},{}\n".format(title, name, role, seiyuu)
        if write is True:
            target.write(row)
        else:
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

def write_to_csv(id_arr, char_target, theme_target):
    """Perform an API call per ID and write onto a csv."""
    total = len(id_arr)
    data = []
    progress = 0
    error = []

    prevData = updateCheck()

    for index, id in enumerate(id_arr):
        result = API_call(id)

        # In case of issues involving timing, retry with a delay
        if result is None and id :
            print("Error - did not get id: {}. Retrying;".format(id))
            time.sleep(1)
            result = API_call(id)

        if result and (id in prevData) and (result == prevData[id]):
            print("Data is similar. Skipping.")
            continue
        else:
            print("No data found or data similar - adding")
            prevData[id] = result


        # If we get a result, keep going
        if result:
            title_eng = result['title_english']
            title = title_eng if title_eng else result['title']

            get_themes(title, result, theme_target, True)
            get_cast(title, result, char_target, True)

        else:
            print("Could not get data.")
            error.append(id)

        # Status update
        print("Complete. {} out of {}.\n".format(index + 1, total))
    if len(error) > 0:
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
    target = open('./output/season-{}'.format(time), 'w')       # Data Write target
    theme_target = open('./output/op-ed-{}'.format(time), 'w')  # OP write target

    write_to_csv(id_arr, target, theme_target)

    print("Script complete. See '{}' for results".format(time))

    return


if __name__ == "__main__":
    main()
