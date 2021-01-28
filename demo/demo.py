# -*- coding: UTF-8 -*-
from desscription_tag_maker.maker import Maker

maker = Maker()
url = 'https://news.infoseek.co.jp/article/20180526hochi235/'

sentences = maker.make_from_web(url, 3, 'div', {'class': 'topic-detail__text'})

file = open("result.txt","w") 
file.write(sentences[0].encode('utf-8'))
file.write(sentences[1].encode('utf-8'))
file.write(sentences[2].encode('utf-8'))
file.close()
