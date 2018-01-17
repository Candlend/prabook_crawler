import xlrd
from xlutils.copy import copy
import sys
import crawler

rdata = xlrd.open_workbook(sys.argv[1])
wdata = copy(rdata)
rtable = rdata.sheets()[0]
wtable = wdata.get_sheet(0)
nrows = rtable.nrows
start = int(input("start: "))-1
end = int(input("end: "))
path = input('save position: ')
for i in range(start,end):
    name = rtable.row_values(i)[2]
    print ("Crawling... "+ name)
    celebrity = crawler.crawl(name)
    print (celebrity)
    print ("Get!")
    wtable.write(i,6,celebrity['Background'])
    wtable.write(i,7,celebrity['Birthday'])
    wtable.write(i,8,celebrity['Birthplace'])
    wtable.write(i,9,celebrity['Foreign'])
    wtable.write(i,10,celebrity['Education'])
    wtable.write(i,11,celebrity['Career'])
    wtable.write(i,12,celebrity['Personality'])
    wtable.write(i,13,celebrity['Connections-Married'])
    wtable.write(i,14,celebrity['father'])
    wtable.write(i,15,celebrity['mother'])
    wtable.write(i,16,celebrity['spouse'])
    wtable.write(i,17,celebrity['how many children'])
    wtable.write(i,18,celebrity['children'])
wdata.save(path)
