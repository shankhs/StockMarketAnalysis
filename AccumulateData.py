# More info on url fields: http://finance.yahoo.com/d/quotes.csv?s=AAPL+GOOG+MSFT&f=nab
# Symbols were taken from here: ftp://ftp.nasdaqtrader.com/SymbolDirectory/
# Right now this script only fetches max and min value of stocks for one day. 

import urllib2
import sys

class Company:
	symbol=""
	securityName=""
	marketCategory=""
	testIssue=""
	financialStatus=""
	roundLotsize=""
	metaInfo=""
	def __init__(self, symbol, securityName,marketCategory,testIssue,financialStatus,roundLotsize,metaInfo):
		self.symbol = symbol
		self.securityName = securityName
		self.marketCategory = marketCategory
		self.testIssue = testIssue
		self.financialStatus = financialStatus
		self.roundLotsize = roundLotsize
		self.metaInfo = metaInfo
	def printClassFields(self):
		print(metaInfo.split('|'),'\n')
		print(self.symbol,self.securityName,self.marketCategory,self.testIssue,self.financialStatus,self.roundLotsize)

def getData(stock, period):
        url = 'http://ichart.finance.yahoo.com/table.csv?s='+stock+'&a=00&b=1&c=1900&d=11&e=31&f=2015&g='+period+'&ignore=.csv'
        page = urllib2.urlopen(url).read()
        filename = stock+'.csv'
        with open(filename, 'w') as f:
                f.write(page)
        
def getSymbols(symbolFile):
	symbolsInfo = [s for s in open(symbolFile)]
	symbols=[]
	lineNumber = 0
	metaInfo=""
	nasdaqSyms=[]
	for info in symbolsInfo:
		if lineNumber == 0:
			metaInfo = info
		elif lineNumber == len(symbolsInfo)-1:
			break
		else:
			info = info.split('|')
			#print info
			if len(info)!=6:
				print 'Error Encountered'
				break
			symbol = info[0]
			securityName = info[1]
			marketCategory = info[2]
			testIssue = info[3]
			financialStatus = info[4]
			roundLotsize = info[5]
			comp = Company(symbol,securityName,marketCategory,testIssue,financialStatus,roundLotsize,metaInfo)
			symbols.append(comp)
			#raw_input()
		lineNumber +=1
	#for syms in symbols:
		#nasdaqSyms.append(syms.symbol)
		#print syms.symbol
	return symbols

def writeStockInfo(stockCsv,outFile):
	stockFile = open(outFile,"w")
	for stock in stockCsv:
		stockFile.write(stock)
		stockFile.write('\n')
	stockFile.close()

if __name__=='__main__':
	if len(sys.argv)<2:
		print 'Enter file to write the stock info'
	else:
		symbolFile = 'nasdaqlisted.txt'
		symbols = getSymbols(symbolFile)
		totalStocks=0
		stockCsv = []
		for syms in symbols:
			print 'Fetching stock info for ',syms.symbol,' ',syms.securityName
			url = 'http://finance.yahoo.com/d/quotes.csv?s='+syms.symbol+'&f=sgh'
			response = urllib2.urlopen(url)
			html = response.read()
			#print html
			stockCsv.append(html)
			response.close();
			totalStocks+=1
		print 'Total ',totalStocks,' number of stock info retrieved'
		print 'Writing to file: ',sys.argv[1]
		writeStockInfo(stockCsv,sys.argv[1])
