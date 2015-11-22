#!/usr/bin/env python3
import urllib.request
import sys
import os
import re
import getopt
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--add", nargs='+', help="add a symbol, the quantity held and the price paid")
parser.add_argument("--delete", help="delete a symbol")
args = parser.parse_args()

if args.add:
     if len(args.add)!=3:
          print('symbol, quantity and price are required with --add')
          sys.exit(1)

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

if os.path.exists('stocks.npy')==False:
     stocks={}
else:
     stocks = np.load('stocks.npy').item()
if os.path.exists('cost.npy')==False:
     cost={}
else:
     cost = np.load('cost.npy').item()
value = cost.copy()
day = cost.copy()

def inputtostocks(sym, qtn, price):
     url = "http://download.finance.yahoo.com/d/quotes.csv?s="+sym+"&f=ac"
     f = urllib.request.urlopen(url)
     r = f.read()
     if len(r)<10:
          print(sym + ' is not a valid stock symbol')
          return
     if (str(r)[2])=='N':
          print(sym + ' is not a valid stock symbol')
          return
     paid=int(qtn*price)
     stocks.update({sym:qtn})
     np.save('stocks.npy', stocks) 
     cost.update({sym:paid})
     np.save('cost.npy', cost)
     
def removestocks(sym):
     if sym in stocks:
          del stocks[sym]
          np.save('stocks.npy', stocks) 
     if sym in cost:
          del cost[sym]
          np.save('cost.npy', cost)
     return

def getcurrentprice(symbol):
     url = "http://download.finance.yahoo.com/d/quotes.csv?s="+symbol+"&f=ac"
     f = urllib.request.urlopen(url)
     r = f.read()
     r = (r.decode("utf-8").strip())
     data=re.sub(r'\s', '',r).split(',')
     s=float(data[0])
     change=((data[1][2:7]).strip('-'))
     if (data[1][1])=='-':
          change=float('-'+change)
     day[symbol]=(float(change)*(stocks[symbol]))
     value[symbol] =((stocks[symbol])*(s))
     print('{:<4} {:<8} {:<14} {:<16} {:<16}'.format
           (symbol,
            ' $'+str(s),
            str((data[1]).strip('"')),
            'value $'+ str(round((stocks[symbol])*(s),2)),
            'gain $'+ str(round(((stocks[symbol])*(s)) -(cost[symbol]),2))),
            '%'+ str(round(100*((((stocks[symbol])*(s)) - (cost[symbol]))/(cost[symbol])),2)))

if args.add:
     sym=str(args.add[0])
     qtn=int(args.add[1])
     price=float(args.add[2])
     inputtostocks(sym,qtn,price)
     
if args.delete:
     sym=str(args.delete)
     removestocks(sym)

if len(stocks)==0:
     print('Please input stocks with --add')
     sys.exit(1)

for key in sorted(stocks.keys()):
	getcurrentprice(key)

gain=sum(day.values())
mkt=sum(value.values())
cst=sum(cost.values())

print()
print('Day Change =  $'+str(round(gain,2)) +
     ', %' + str(round(((mkt-gain)/mkt),2)))
print('Totals: Cost $' + str(cst) +
       ' Value $' + str(round(mkt,2)) +
       ' Gain $' + str(round((mkt-cst),2)) +
       ', %' + str(round((100*(mkt-cst)/cst),2)))
       
