import urllib.request
import json

def API_call(MAL_id):
    '''
    The API call using jikan.moe instead of the official API for ease of use.
    May change this later on.
    '''

    API_url = "http://api.jikan.moe/anime/{}/characters_staff".format(MAL_id)
    data = urllib.request.urlopen(API_url).read()

    decoded_data = json.loads(data.decode('utf-8'))
    return decoded_data['character']

def main():
    '''
    Main function; meant to grab all the MAL IDs from a file, then grab
    character data from each one. For the time being, I'll just grab it
    from plaintext.
    '''

    chardata = API_call(23)
    for character in chardata:
        print(character['name'], character['role'])



if __name__== "__main__":
    main()
