import urllib.request
import json
import sys
from html import unescape
import time


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
        return None, None

    result = json.loads(data.read())

    if result['title_english']:
        return unescape(result['title_english']), result['character']
    elif result['title']:
        return unescape(result['title']), result['character']
    else:
        return None, None


def ID_get(file):
    """Grabs all MAL IDs from a text file."""
    inputfile = open(file).read()
    return inputfile.split("\n")


def write_to_csv(id_arr, target):
    """Perform an API call per ID and write onto a csv."""
    total = len(id_arr)
    progress = 0
    error = []
    for id in id_arr:
        progress += 1
        title, chardata = API_call(id)
        # Status check
        print("Getting info from {}, id: {}".format(title, id))
        if title is None:
            print("Error - did not get id: {}. Retrying;".format(id))
            time.sleep(1)
            title, chardata = API_call(id)

        if title and chardata:
            for char in chardata:
                # TODO: More efficient way instead of double unescapes
                role = char['role']
                name = unescape(unescape(char['name']))
                if(char['voice_actor']):
                    seiyuu = unescape(unescape(char['voice_actor'][0]['name']))
                else:
                    seiyuu = "N/A"

                # Cleaned up array for writing into csv
                row_array = "{},{},{},{}\n".format(title, name, role, seiyuu)

                # Proper CSV
                target.write(row_array)
        else:
            print("Could not get data.")
            error.append(id)

        # Status update
        print("Complete. {} out of {}.\n".format(progress, total))

    if len(error) > 0:
        print("Could not get IDs: {}".format(error))


def main():
    """Perform main function."""
    if len(sys.argv) != 3:
        print("Usage: python index.py [file with ID input] [csv output]")
        return None

    print("Script beginning - pulling IDs")
    file_source = sys.argv[1]           # Source of IDs
    file_target = sys.argv[2]           # Target of data we want

    id_arr = ID_get('./input/{}'.format(file_source))        # ID Read target
    target = open('./output/{}'.format(file_target), 'w')   # Data Write target

    write_to_csv(id_arr, target)        # Loop function for writing

    print("Script complete. See '{}' for results".format(file_target))
    return


if __name__ == "__main__":
    main()
