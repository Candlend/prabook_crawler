# -*- coding: utf-8 -*-

from lxml import etree
import requests
import time
import json
import regex as re
import Levenshtein

def crawl(name):
    switch = 0
    celebrity = {'Education':'','Personality':'','Background':'','Birthday':'','Birthplace':'','Foreign':'','Career':'','Connections-Married':'', \
    'father':'','mother':'','spouse':'','how many children':'','children':'','name':''}
    url= "https://prabook.com/web/search.json"
    p={'general':name,'_dc':int(time.time()),'start':0,'rows':5}
    r1=requests.get(url,params=p)
    reliability = 0
    for eachresult in r1.json()['result']:
        celebrity['name']= eachresult["fullName"].replace("<mark>","").replace("</mark>","")
        eachreliability = Levenshtein.ratio(celebrity['name'].lower().replace('.',''),name.lower().replace('.',''))
        if eachreliability > reliability:
            reliability = eachreliability
            j = eachresult
        print (celebrity['name'])
    print ('reliability: %.2f%%' % (reliability*100))
    celebrity['Background']=j["staticBackground"]
    celebrity['Birthday']="%d/%d/%d" % (j["birthYear"],j["birthMonth"],j["birthDay"])
    celebrity['Birthplace']=j["birthPlace"]
    if j["nationalities"][0] == "American":
        celebrity['Foreign'] = 'N'
    else:
        celebrity['Foreign'] = 'Y'
    path="https://prabook.com/web" + j["seoUrl"]
    r2=requests.get(path)
    html = r2.text.encode("utf-8")
    tree = etree.HTML(html)
    links = tree.xpath('//article[@class="article__item"]')
    if len(links) == 0:
        print ("no article")
        return celebrity
    try:
        Interests=tree.xpath('//p[@class="interest-list__element"]/text()')[0]
        celebrity["Personality"]=Interests.replace("\r","").replace("\n","").replace("\t","").replace("â","—")
    except:
        print ("no interest")
    for eachlink in links:
        title1 = eachlink.xpath('h3[@class="article__title"]/text()')[0].replace("\r","").replace("\n","").replace("\t","")
        if title1 == "Education" or title1 == "Career" or title1 == "Background":
            text = eachlink.xpath('p[@class="article__text"]/text()')[0].replace("\r","").replace("\n","").replace("\t","").replace("â","—")
            if celebrity[title1] == '':
                celebrity[title1]=text
        if title1 == "Connections":
            try:
                text = eachlink.xpath('p[@class="article__text"]/text()')[0].replace("\r","").replace("\n","").replace("\t","").replace("â","—")
                married = re.findall(r'(?<=Married[^\d:;]+?, )[^.]*(?=.)',text)
                if len(married) == 1:
                    celebrity["Connections-Married"] = married[0]
                else:
                    print ("something wrong %d" % len(married))
            except IndexError:
                print ("He has no wife.")
            links2 = eachlink.xpath('dl[@class="def-list"]')
            for eachlink2 in links2:
                try:
                    title2 = eachlink2.xpath('dt[@class="def-list__title"]/text()')[0].replace("\r","").replace("\n","").replace("\t","")
                except IndexError:
                    # print ("no title")
                    pass
                #     text = eachlink2.xpath('dd[@class="def-list__text"]/text()')[0].replace("\r","").replace("\n","").replace("\t","").replace("â","—").strip()
                #     if switch == 1:
                #         celebrity["children"] = celebrity["children"] + "; " + text
                #         celebrity["how many children"] += 1
                #     else:
                #         celebrity["spouse"] = celebrity["spouse"] + "; " + text
                if title2 == "father:" or title2 == "mother:" or title2 == "spouse:" or title2 == "children:" or title2 == "spouses:":
                    text = eachlink2.xpath('dd[@class="def-list__text"]/text()')[0].replace("\r","").replace("\n","").replace("\t","").replace("â","—").strip()
                    if title2 == "spouses":
                        if celebrity["spouse"] == "":
                            celebrity["spouse"] = text
                        else:
                            celebrity["spouse"] += "; " + text
                    else:
                        if celebrity[title2[:-1]] == "":
                            celebrity[title2[:-1]] = text
                        else:
                            celebrity[title2[:-1]] += "; " + text
                        # print (text)
                        if title2 == "children:":
                            if celebrity["how many children"] == "":
                                celebrity["how many children"] = 1
                            else:
                                celebrity["how many children"] += 1

        else:
            continue

    return (celebrity)


if __name__ == '__main__':
    name = input('name: ')
    celebrity = crawl(name)
    print (json.dumps(celebrity,sort_keys=True, indent=4, separators=(',', ': ')))
