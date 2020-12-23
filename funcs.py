import random
import requests
import json
import os

from TikTokApi import TikTokApi

api = TikTokApi.get_instance(use_selenium=True)


def find_trending_hashtags():
    hashtags = api.discoverHashtags()
    chosen_hashtag = random.choice(hashtags)['cardItem']['title']
    videos_by_hashtag = api.byHashtag(chosen_hashtag, count=20)
    chosen_video = random.choice(videos_by_hashtag)
    music_author = str(chosen_video['music']['authorName'])
    music_name = str(chosen_video['music']['title'])
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

    return filename, username, music_author, music_name


def clear():
    for file in os.listdir(os.getcwd()):
        if file.endswith('.mp4'):
            os.remove(file)


def find_hashtag_video(tag):
    hashtags = api.byHashtag(tag, count=10)
    cvideo = random.choice(hashtags)
    music_author = str(cvideo['music']['authorName'])
    music_name = str(cvideo['music']['title'])
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

    return filename, username, music_author, music_name


def find_trending_music():
    music = api.discoverMusic()
    chosen_music = random.choice(music)
    videos_by_music = api.bySound(chosen_music['cardItem']['id'], count=20)
    chosen_video = random.choice(videos_by_music)
    music_author = str(chosen_video['music']['authorName'])
    music_name = str(chosen_video['music']['title'])
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

    return filename, username, music_author, music_name
