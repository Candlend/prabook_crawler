from lxml import etree
import requests
import time
import json

celebrity = {}
# name=input('name:')
celebrity['name']='Harold A. Wagner'
url= "https://prabook.com/web/search.json"

# print(url)
p={'general':celebrity['name'],'_dc':int(time.time()),'start':0,'rows':1}
# print (p)
r1=requests.get(url,params=p)
j=r1.json()['result'][0]
path="https://prabook.com/web" + j["seoUrl"]
celebrity['background']=j["staticBackground"]
celebrity['birthday']="%d/%d/%d" % (j["birthYear"],j["birthMonth"],j["birthDay"])
celebrity['birthplace']=j["birthPlace"]
if j["nationalities"][0] == "American":
    celebrity['foreign'] = 'Y'
else:
    celebrity['foreign'] = 'N'

print (celebrity)
r2=requests.get(path)
# print(r2.url)
j = json.dumps(r1.json(),sort_keys=True, indent=4, separators=(',', ': '))
print (j)

# html = r.text.encode("utf-8")
# print (html)
# tree = etree.HTML(html)
# links = tree.xpath('//@href')
# # links = tree.xpath('//div[@class="body"]/div[@class="content-wrapper-search clf"]/div[@class="content"] \
# # /div[@class="layout-grid layout-grid_content"]/div[@class="layout-grid__col layout-grid__col_content"] \
# # /div[@id="search-results"]/div[@id="results" and @class="search-results"]')
# print (links)
#
# for i in links:
#     print(i)
