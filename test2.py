from bs4 import BeautifulSoup
import pandas as pd
import json
import os
import requests

url = input('https://www.youtube.com/watch?v=XjNm9bazxn8 ')
Vid = {}
Link = url
source = requests.get(url).text
soup = BeautifulSoup(source, 'lxml')
div_s = soup.findAll('div')

Title = div_s[1].find('span', class_='watch-title').text.strip()
Vid['Title'] = Title
Vid['Link'] = Link
Channel_name = div_s[1].find('a', class_="yt-uix-sessionlink spf-link").text.strip()
Channel_link = ('www.youtube.com' + div_s[1].find('a', class_="yt-uix-sessionlink spf-link").get('href'))
Subscribers = div_s[1].find('span',
                            class_="yt-subscription-button-subscriber-count-branded-horizontal yt-subscriber-count").text.strip()
if len(Channel_name) == 0:
    Channel_name = 'None'
    Channel_link = 'None'
    Subscribers = 'None'
Vid['Channel'] = Channel_name
Vid['Channel_link'] = Channel_link
Vid['Channel_subscribers'] = Subscribers

Category_index = {
    1: 'Film & Animation',
    2: 'Autos & Vehicles',
    10: 'Music',
    15: 'Pets & Animals',
    17: 'Sports',
    19: 'Travel & Events',
    20: 'Gaming',
    22: 'People & Blogs',
    23: 'Comedy',
    24: 'Entertainment',
    25: 'News & Politics',
    26: 'Howto & Style',
    27: 'Education',
    28: 'Science & Technology',
    29: 'Nonprofits & Activism'}
Sp = div_s[1].text.split(':')
subs = 'categoryId'
for j in range(len(Sp)):
    if subs in Sp[j]:
        value = int(Sp[j + 1].split(',')[0])
Video_category = Category_index[value]
Vid['Category'] = Video_category

View_count = div_s[1].find(class_='watch-view-count')
View_count = View_count.text.strip().split()[0]
Vid['Views'] = View_count

Likes = div_s[1].find('button',
                      class_="yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-like-button like-button-renderer-like-button-unclicked yt-uix-clickcard-target yt-uix-tooltip").text.strip()
Vid['Likes'] = Likes
Dislikes = div_s[1].find('button',
                         class_="yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-dislike-button like-button-renderer-dislike-button-unclicked yt-uix-clickcard-target yt-uix-tooltip").text.strip()
Vid['Dislikes'] = Dislikes

Related_videos = div_s[1].findAll('a', class_='content-link spf-link yt-uix-sessionlink spf-link')
Title_Related = []
Link_Related = []
for i in range(len(Related_videos)):
    Title_Related.append(Related_videos[i].get('title'))
    Link_Related.append(Related_videos[i].get('href'))
Related_dictionary = dict(zip(Title_Related, Link_Related))
Vid['Related_vids'] = Related_dictionary

print('Title of the video url:', Title)
print('Channel :', Channel_name)
print('Link:', Channel_link)
print('Number of Subscibers:', Subscribers)
print('Category for the video url:', Video_category)
print('View count for the video url:', View_count)
print('Likes:', Likes, '  ', 'Dislikes:', Dislikes)

with open('vfile.json', 'w', encoding='utf8') as ou:
    json.dump(Vid, ou, ensure_ascii=False)
