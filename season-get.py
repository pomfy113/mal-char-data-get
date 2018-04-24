import urllib.request
import sys
import json


def main():
    """Grab list of IDs using unoffocial MAL API (Jikan)."""

    if len(sys.argv) != 3:
        print("Usage: python season-get [year] [season, lowercase]")
        return None

    year = sys.argv[1]
    season = sys.argv[2]
    print("Pulling from API")

    API_url = "http://api.jikan.moe/season/{}/{}".format(year, season)

    # Error checking
    try:
        data = urllib.request.urlopen(API_url)
    except urllib.error.URLError as e:
        print("Error - {}".format(e))
        return None
    print("Complete!\n")

    result = json.loads(data.read())['season']

    print("Loading IDs")
    target_name = '{}-{}.txt'.format(year, season)
    target = open('./input/{}'.format(target_name), 'w')

    for anime in result:
        target.write(str(anime['mal_id']) + '\n')
    print("Complete!\n")


if __name__ == "__main__":
    main()
