# -*- coding: utf-8 -*-

from lxml import etree
import requests
import time
import json
import re

celebrity = {}
# name=input('name:')
celebrity['name']='Harold A. Wagner'
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
# path="https://prabook.com/web/harold_a.wagner/523210"
r2=requests.get(path)
# print(r2.url)0
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
    title1 = eachlink.xpath('h3[@class="article__title"]/text()')[0].replace("\r","").replace("\n","").replace("\t","")
    # x=etree.tostring(title1,pretty_print=True).decode()
    # print(type(title1))
    print(title1)
    if title1 == "Education" or title1 == "Career" or title1 == "Background":
        text = eachlink.xpath('p[@class="article__text"]/text()')[0].replace("\r","").replace("\n","").replace("\t","").replace("â","—")
        # print(type(text))
        # print(text)
    if title1 == "Connections":
        text = eachlink.xpath('p[@class="article__text"]/text()')[0].replace("\r","").replace("\n","").replace("\t","").replace("â","—")
        celebrity["Connections-Married"]=re.findall(r'(?<=Married\D+?, )[^.]*(?=.)',text)[0]
        links2 = eachlink.xpath('dl[@class="def-list"]')
        print(links2)
        for eachlink2 in links2:
            try:
                title2 = eachlink2.xpath('dt[@class="def-list__title"]/text()')[0].replace("\r","").replace("\n","").replace("\t","")
            except:
                text = eachlink2.xpath('dd[@class="def-list__text"]/text()')[0].replace("\r","").replace("\n","").replace("\t","").replace("â","—").strip()
                celebrity["children"] = celebrity["children"] + "; " + text
                celebrity["how mang children"] += 1
                continue
            if title2 == "father:" or title2 == "mother:" or title2 == "spouse:" or title2 == "children:":
                text = eachlink2.xpath('dd[@class="def-list__text"]/text()')[0].replace("\r","").replace("\n","").replace("\t","").replace("â","—").strip()
                celebrity[title2[:-1]] = text
                if title2 == "children:":
                    celebrity["how mang children"] = 1
                continue

    else:
        continue
    if title1 not in celebrity.keys():
        celebrity[title1]=text
print (celebrity)
print (json.dumps(celebrity,sort_keys=True, indent=4, separators=(',', ': ')))
# # links = tree.xpath('//div[@class="body"]/div[@class="content-wrapper-search clf"]/div[@class="content"] \
# # /div[@class="layout-grid layout-grid_content"]/div[@class="layout-grid__col layout-grid__col_content"] \
# # /div[@id="search-results"]/div[@id="results" and @class="search-results"]')
# print (links)
#
# for i in links:
#     print(i)
