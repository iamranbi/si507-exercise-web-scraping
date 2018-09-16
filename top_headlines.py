# Ran Bi
import requests
from bs4 import BeautifulSoup


print('Top Headlines\n')

##news
index=[1,4,7,10,13,16,19,22,25,28]
ht_news="https://www.michigandaily.com/section/news"
html_news=requests.get(ht_news).text
soup_news=BeautifulSoup(html_news, 'html.parser')
news=soup_news.find_all('div', class_='field-content')
news_heads=[]
for i in index:
    n=news[i].find('a').contents[0]
    if n in ('',' ','  ','   '):
        n='missing headline'
    news_heads.append(n)

##sports
ht_sports="https://www.michigandaily.com/section/sports"
html_sports=requests.get(ht_sports).text
soup_sports=BeautifulSoup(html_sports, 'html.parser')
sports=soup_sports.find_all('div', class_='field-content')
sports_heads=[]
for i in index:
    n1=sports[i].find('a').contents[0]
    if n1 in ('',' ','  ','   '):
        n1='missing headline'
    sports_heads.append(n1)

##arts
ht_arts="https://www.michigandaily.com/section/arts"
html_arts=requests.get(ht_arts).text
soup_arts=BeautifulSoup(html_arts, 'html.parser')
arts=soup_arts.find_all('div', class_='field-content')
arts_heads=[]
for i in index:
    n2=arts[i].find('a').contents[0]
    if n2 in ('',' ','  ','   '):
        n2='missing headline'
    arts_heads.append(n2)


##print
print('Top 10 Headlines: news')
for i in news_heads:
    print(i)

print('\n')
print('Top 10 Headlines: sports')
for i in sports_heads:
    print(i)

print('\n')
print('Top 10 Headlines: arts')
for i in arts_heads:
    print(i)
