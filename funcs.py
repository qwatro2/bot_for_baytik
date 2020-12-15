import random
import requests
import json
import os

from TikTokApi import TikTokApi

api = TikTokApi.get_instance(use_selenium=True)

def get_trending_hashtags():
    hashtags = api.discoverHashtags()
    chosen_hashtag = random.choice(hashtags)['cardItem']['title']
    videos_by_hashtag = api.byHashtag(chosen_hashtag, count=20)
    chosen_video = random.choice(videos_by_hashtag)
    
    username = str(chosen_video['author']['uniqueId'])
    video_id = chosen_video['id']
    url = 'https://www.tiktok.com/@{}/video/{}'.format(username, video_id)
    payload = {'url': url}
    tikfail_url = 'https://tik.fail/api/geturl'
    r = requests.post(tikfail_url, data=payload)
    rdata = json.loads(r.text)
    direct = rdata.get('direct')
    recfile = requests.get(direct)
    filename = str(video_id) + '.mp4'
    with open(filename, 'wb') as video:
        video.write(recfile.content)

    return filename

def clear():
    for file in os.listdir(os.getcwd()):
        if file.endswith('.mp4'):
            os.remove(file)

def find_hashtag_video(tag):
    hashtags = api.byHashtag(tag, count=10)
    cvideo = random.choice(hashtags)
    username = str(cvideo['author']['uniqueId'])
    video_id = cvideo['id']
    url = 'https://www.tiktok.com/@{}/video/{}'.format(username, video_id)
    payload = {'url': url}
    tikfail_url = 'https://tik.fail/api/geturl'
    r = requests.post(tikfail_url, data=payload)
    rdata = json.loads(r.text)
    direct = rdata.get('direct')
    recfile = requests.get(direct)
    filename = str(video_id) + '.mp4'
    with open(filename, 'wb') as video:
        video.write(recfile.content)

    return filename

def find_trending_music():
    music = api.discoverMusic()
    chosen_music = random.choice(music)
    r = requests.get(chosen_music['cardItem']['extraInfo']['playUrl'][0])
    name = str(chosen_music['cardItem']['title']) + '.mp3'
    with open(name, 'wb') as music:
        music.write(r.content)





