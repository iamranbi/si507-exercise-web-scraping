import requests
import json
from bs4 import BeautifulSoup

## Code for Caching:
# try to load the cache from file
CACHE_FNAME='umsi_member_cache.json'
try:
    cache_file=open(CACHE_FNAME, 'r')
    cache_contents=cache_file.read()
    CACHE_DICTION=json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION={}

def make_request_using_cache(url):
    if url in CACHE_DICTION:
        return CACHE_DICTION[url]
    else:
        header={'User-Agent': 'SI_CLASS'}
        re_page=requests.get(url, headers=header).text
        CACHE_DICTION[url]=re_page
        dumped_json_cache=json.dumps(CACHE_DICTION)
        fw=open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[url]

## Define the class
class People:
    def __init__(self, name, title, node):
        self.name=name
        self.title=title
        self.node=node
        detail_url='https://www.si.umich.edu'+node
        page_text=make_request_using_cache(detail_url)
        page_soup=BeautifulSoup(page_text, 'html.parser')
        page_field=page_soup.find_all(class_='field-item even')
        for i in page_field:
            if i.text.endswith('.edu'):
                self.email=i.text

## Access each page of the directory, get the HTML and create a dictionary 
def get_umsi_data(page):
    # fetch data from cache
    base='https://www.si.umich.edu/directory?rid=All&page='
    baseurl=base+str(page)
    re=make_request_using_cache(baseurl)
    soup=BeautifulSoup(re, 'html.parser')
    soup_content=soup.find_all(class_='field-item even')
    name_title=[]
    contact=[]
    list_people=[]
    umsi_titles=dict()
    for i in soup_content:
        # extract personal node--personal homepage
        if i.text=='Contact Details\n':
            c=i.find('a')['href']
            contact.append(c)
        # extract name and title
        elif not i.text.endswith('\n'):
            name_title.append(i.text)
    name=name_title[::2]
    title=name_title[1::2]
    # create People instance for each people
    for i in range(len(name)):
        p=People(name[i],title[i],contact[i])
        list_people.append(p)
    # convert to dict
    for i in list_people:
        if i.name in umsi_titles:
             i.name=i.name+' '+i.title[0:3]
        umsi_titles[i.name]=dict()
        umsi_titles[i.name]['title']=i.title
        umsi_titles[i.name]['email']=i.email
    return (umsi_titles)

## Create the dictionary: key is name of each person in the UMSI directory; value is that person's title and email
directory_dict=dict()
for i in range(13):
    new_dict=get_umsi_data(i)
    directory_dict.update(new_dict)

## Write out the dictionary to a file
with open('directory_dict.json', 'w') as outfile:
    json.dump(directory_dict, outfile)
