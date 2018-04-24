import urllib.request
import json
import sys
from html import unescape


def API_call(MAL_id):
    """Calls jikan.moe instead of the official MAL API for ease of use.
    May change this later on."""

    API_url = "http://api.jikan.moe/anime/{}/characters_staff".format(MAL_id)

    try:
        data = urllib.request.urlopen(API_url)
    except urllib.error.URLError as e:
        return None

    result = json.loads(data.read())
    return result['character']


def ID_get(file):
    """Grabs all MAL IDs from a text file."""
    inputfile = open(file).read()
    return inputfile.split()


def main():
    """Perform main function."""
    if len(sys.argv) != 3:
        print("Format: python index.py [file with ID input] [csv output]")
        return

    source_id = sys.argv[1]
    id_arr = ID_get(source_id)

    for id in id_arr:
        chardata = API_call(id)
        if chardata:
            for character in chardata:
                print(unescape(character['name']), character['role'])

if __name__== "__main__":
    main()
