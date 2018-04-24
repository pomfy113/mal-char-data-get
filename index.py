import urllib.request
import json

API_url = "http://api.jikan.moe/anime/1/characters_staff"
API_content = urllib.request.urlopen(API_url)

data = API_content.read()
decoded_data = json.loads(data.decode('utf-8'))

print(decoded_data['character'])
