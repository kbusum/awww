#
# Author : Kwame Busumtwi
# Python script to download MP3 files and Soundcloud A Way With Words podcast
#
# https://stackoverflow.com/questions/59539194/how-to-download-all-mp3-url-as-mp3-from-a-webpage-using-python3
#
import requests
from bs4 import BeautifulSoup
import re
from sclib import SoundcloudAPI, Track, Playlist
import urllib.request

def download_all_podcast(url):
    url=url
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    pd_title = soup.find_all('h2', class_='entry-title')
    global epi
    for j in reversed(range(0, len(pd_title))):
        tmp_ttitle = pd_title[j].text.replace(" ", "_")
        
        epi_url =pd_title[j].find('a').get('href')
        epi_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        epi_response = requests.get(epi_url, headers=epi_headers)
        epi_soup = BeautifulSoup(epi_response.text, 'lxml')
        epi_dl = epi_soup.find_all('div', class_='entry_content')
        
        snd_dl=epi_dl[0].find('a', href=re.compile('soundcloud'))
        mp3_dl = epi_dl[0].find('a', href=re.compile('mp3'))

        if (snd_dl is not None):
            #
            # This code will run if there is a Soundcloud link
            #
            print(str(epi) + '_'+ tmp_ttitle)
            print(snd_dl.get('href'))
            api = SoundcloudAPI()  # never pass a Soundcloud client ID that did not come from this library
            track = api.resolve(snd_dl.get('href'))
            with open(str(epi) + '_'+ tmp_ttitle + '.mp3', 'wb+') as fp:
                track.write_mp3_to(fp)

        elif (mp3_dl is not None):
            #
            # This code will run if there is an Mp3 link
            #
            print(str(epi) + '_'+ tmp_ttitle)
            print(mp3_dl.get('href'))
            doc = requests.get(mp3_dl.get('href'))
            with open(str(epi) + '_'+ tmp_ttitle + '.mp3', 'wb') as f:
                f.write(doc.content)
        else:
            #
            # This code will run if there No Link
            #
            print('sorry no audio file found')
        
        epi+=1
    print('\n')

#
# Main Program starts here
#
epi=0
for i in reversed(range(1,75)):
    print("https://www.waywordradio.org/category/episodes/page/" + str(i))
    print('**********************************')
    download_all_podcast("https://www.waywordradio.org/category/episodes/page/" + str(i))