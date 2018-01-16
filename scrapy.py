# -*- coding: utf-8 -*-

from lxml import etree
import requests
import time
import json

celebrity = {}
# name=input('name:')
celebrity['Name']='Harold A. Wagner'
url= "https://prabook.com/web/search.json"

p={'general':celebrity['name'],'_dc':int(time.time()),'start':0,'rows':1}
r1=requests.get(url,params=p)
j=r1.json()['result'][0]
celebrity['Background']=j["staticBackground"]
celebrity['Birthday']="%d/%d/%d" % (j["birthYear"],j["birthMonth"],j["birthDay"])
celebrity['Birthplace']=j["birthPlace"]
if j["nationalities"][0] == "American":
    celebrity['Foreign'] = 'Y'
else:
    celebrity['Foreign'] = 'N'

path="https://prabook.com/web" + j["seoUrl"]
path="https://prabook.com/web/harold_a.wagner/523210"
r2=requests.get(path)
# print(r2.url)
# j = json.dumps(r1.json(),sort_keys=True, indent=4, separators=(',', ': '))
# print (j)
html = r2.text.encode("utf-8")
# print (html)
tree = etree.HTML(html)
links = tree.xpath('//article[@class="article__item"]')
Interests=tree.xpath('//p[@class="interest-list__element"]/text()')[0]
# print (Interests)
celebrity["Interests"]=Interests.replace("\r","").replace("\n","").replace("\t","").replace("â","—")
# print (links)
for eachlink in links:
    # print(dir(eachlink))
    title = eachlink.xpath('h3[@class="article__title"]/text()')[0].replace("\r","").replace("\n","").replace("\t","")
    # x=etree.tostring(title,pretty_print=True).decode()
    # print(type(title))
    # print(title)
    if title == "Education" or title == "Career" or title == "Background":
        text = eachlink.xpath('p[@class="article__text"]/text()')[0].replace("\r","").replace("\n","").replace("\t","").replace("â","—")
        # print(type(text))
        # print(text)
    if title == "Connections":
        pass
    else:
        continue
    if title not in celebrity.keys():
        celebrity[title]=text
print (celebrity)
print (json.dumps(celebrity,sort_keys=True, indent=4, separators=(',', ': ')))
# # links = tree.xpath('//div[@class="body"]/div[@class="content-wrapper-search clf"]/div[@class="content"] \
# # /div[@class="layout-grid layout-grid_content"]/div[@class="layout-grid__col layout-grid__col_content"] \
# # /div[@id="search-results"]/div[@id="results" and @class="search-results"]')
# print (links)
#
# for i in links:
#     print(i)
