import requests, json
from pprint import pprint

api_key = None

def configure_request(app):
    global api_key
    api_key = app.config['API_KEY']

def search(song_title):
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    search_parameters = {
        'key' : api_key,
        'q' : song_title,
        'part' : 'snippet',
        'maxResults' : 10
    }
    res = requests.get(search_url, params=search_parameters)
    results = res.json()['items']
    
    video_ids = []
    video_titles = []

    for item in results:
        video_ids.append(item['id']['videoId'])
        video_titles.append(item['snippet']['title'])
    pprint(video_titles)
    return video_ids