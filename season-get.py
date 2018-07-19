import urllib.request
import json
import os
import re
from html import unescape


def CSV_write(data, year, season):
    target = open('./output-season/{}-{}.csv'.format(year, season), 'w')

    for anime in data['season']:
        title = unescape(anime['title'])
        broadcast = anime['airing_start']
        eps = anime['episodes']
        genres = ", ".join(genre['name'] for genre in anime['genre'])
        studios = ", ".join(unescape(studio['name']) for studio in anime['producer'])

        row = '"{}","{}",{},"{}","{}"\n'.format(title, broadcast, eps, genres, studios)
        target.write(row)

def API_call(year, season):
    """Calls API to get the data."""
    API_url = "http://api.jikan.moe/season/{}/{}/".format(year, season)

    # Error checking
    try:
        data = urllib.request.urlopen(API_url)
    except urllib.error.URLError as e:
        print(e)
        return None

    result = json.loads(data.read())

    return result

def get_input():
    """Helper function; gets user input."""
    year = input('Enter year: ')
    season = input('Enter season (lowercase): ')

    return year, season

def get_time():
    """Gets input from user."""
    # Proper seasons
    season_ok = ['winter', 'spring', 'fall', 'summer']
    print("Looking for seasonal info.\n")

    # Loop until proper input
    while True:
        year, season = get_input()
        if season in season_ok and year.isdigit():
            break;
        else:
            print("Invalid input. Try again.\n")

    return year, season

def main():
    """Perform main function."""
    # Main loop
    while True:
        # See if it's a valid season; if not, retry input
        year, season = get_time()
        # Initial pass through done; now we can try an API call
        result = API_call(year, season)

        # If issue, try again
        if result is None:
            print("Could not get data, try again.\n")
        else:
            CSV_write(result, year, season)
            break;


if __name__ == "__main__":
    main()
