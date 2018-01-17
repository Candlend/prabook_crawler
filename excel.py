import xlrd
from xlutils.copy import copy
import sys
import crawler
import json
from multiprocessing.dummy import Pool

def process(i):
    name = rtable.row_values(i)[2]
    celebrity = crawler.crawl(name, i, strict, limit)
    # print (json.dumps(celebrity,sort_keys=True, indent=4, separators=(',', ': ')))
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
    wtable.write(i,35,"%.2f%%" % (celebrity["reliability"]*100))
    wtable.write(i,36,name)
    wtable.write(i,37,celebrity['name'])
    wdata.save(path)
    
rdata = xlrd.open_workbook(sys.argv[1])
wdata = copy(rdata)
rtable = rdata.sheets()[0]
wtable = wdata.get_sheet(0)
nrows = rtable.nrows
start = int(sys.argv[3])
end = int(sys.argv[4])+1
if sys.argv[5]:
    print ("use strict")
    strict = 1
else:
    strict = 0
path = sys.argv[2]
limit = float(sys.argv[6])
print ("range: %d~%d" % (int(sys.argv[3]),int(sys.argv[4])))
print ('save position: ' + path)
print ("the lower limit of reliability: ",limit)
pool = Pool(processes=4)
pool.map(process,range(start,end))


