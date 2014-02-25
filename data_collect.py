import urllib2
import time
import httplib

def getData(stock, period):
    url = 'http://ichart.finance.yahoo.com/table.csv?s='+stock+'&a=00&b=1&c=1900&d=11&e=31&f=2015&g='+period+'&ignore=.csv'
    try:
        stream = urllib2.urlopen(url)
        filename = stock+'.csv'
        page = stream.read()
        with open('data/'+filename, 'w') as f:
            f.write(page)
    except urllib2.HTTPError, e:
        print stock+" error"
    except httplib.BadStatusLine:
        print "bad status line"
        time.sleep(120)
        getData(stock, period)


stocks=[]
with open('nasdaqlisted.txt', 'r') as f:
    go = False
    for line in f:
        stock = line.split('|')[0]
        if stock=='Symbol':
            continue
        if stock=='WFBI':
            go = True
        if go:
            getData(stock, 'd')
            time.sleep(.5)
        
