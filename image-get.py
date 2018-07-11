import urllib.request
import json
import os
import re

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
    """Gets input from user."""
    season = input('Enter season (lowercase): ')
    year = input('Enter year: ')

    return year, season

def main():
    """Perform main function."""
    year, season = get_input()

    # See if it's a valid season; if not, retry input
    season_ok = ['winter', 'spring', 'fall', 'summer']
    while season not in season_ok and not year.isdigit():
        print("Invalid input. Try again.\n")
        year, season = get_input()

    # Initial pass through done; now we can try an API call
    result = API_call(year, season)

    # If there's an issue, retry
    while result is None:
        print("Could not get data. Try again.\n")
        year, season = get_input()
        result = API_call(year, season)

    # Directory
    img_dir = "images/{}-{}/".format(season, year)
    if not os.path.isdir(img_dir):
        os.mkdir(img_dir)

    # Going through each anime, then saving
    for anime in result["season"]:
        url = anime["image_url"]
        title = re.sub(r'[\\/*?:"<>|]',"", anime["title"])

        urllib.request.urlretrieve(url, './images/{}-{}/{}.jpg'.format(season, year, title))

if __name__ == "__main__":
    main()
