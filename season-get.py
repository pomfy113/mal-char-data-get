import urllib.request
import sys
import json
from html import unescape


def main():
    """Perform main function."""
    if len(sys.argv) != 3:
        print("Usage: python season-get [year] [season, lowercase]")
    year = sys.argv[1]
    season = sys.argv[2]

    API_url = "http://api.jikan.moe/season/{}/{}".format(year, season)

    try:
        data = urllib.request.urlopen(API_url)
    except urllib.error.URLError as e:
        print("Error - {}".format(e))
        return None

    result = json.loads(data.read())['season']

    target_name = '{}-{}.txt'.format(year, season)
    target = open(target_name, 'w')

    for anime in result:
        target.write(str(anime['mal_id']) + '\n')


if __name__ == "__main__":
    main()
