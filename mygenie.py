from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

import requests
from bs4 import BeautifulSoup

# URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20190908',headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')

# select를 이용해서, tr들을 불러오기
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis (제목)
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis (가수)

musics = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
rank = 0

# musics (tr들) 의 반복문을 돌리기
for music in musics:
    # musics 안에 a 가 있으면,
    title = music.select_one('td.info > a.title.ellipsis').text.strip()
    artist = music.select_one('td.info > a.artist.ellipsis').text
    rank = rank + 1
    if not title == None:
        # db에 저장
        doc = {
            'rank': rank,
            'title': title,
            'artist': artist
        }
        db.musiclist.insert_one(doc)
