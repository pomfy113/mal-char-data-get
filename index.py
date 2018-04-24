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
        return None, None

    result = json.loads(data.read())
    return result['title_english'], result['character']


def ID_get(file):
    """Grabs all MAL IDs from a text file."""
    inputfile = open(file).read()
    return inputfile.split()


def main():
    """Perform main function."""
    if len(sys.argv) != 3:
        print("Usage: python index.py [file with ID input] [csv output]")
        return

    file_source = sys.argv[1]
    file_target = sys.argv[2]
    id_arr = ID_get(file_source)

    target = open(file_target, 'w')

    for id in id_arr:
        title, chardata = API_call(id)
        print("Getting char info from {}".format(title))
        if title and chardata:
            for char in chardata:
                # TODO: More efficient way instead of double unescapes
                role = char['role']
                name = unescape(unescape(char['name']))
                if(char['voice_actor']):
                    seiyuu = unescape(unescape(char['voice_actor'][0]['name']))
                else:
                    seiyuu = "N/A"

                row_array = "{},{},{},{}\n".format(title, name, role, seiyuu)
                target.write(row_array)
        print("Character data from {} complete.".format(title))

    print("Script complete.")
    return

if __name__ == "__main__":
    main()
