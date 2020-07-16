#### Imports ####

import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np





#### Joao Inverno API test area #### 

list_stock=["ZM","ZOOM"]#,"APPL","GOOGL","AMZN","MSFT","NVDA"]


url="https://www.alphavantage.co/query?"

daily_stock_df=pd.DataFrame()
stocks=[]
for stock in list_stock:

    stocks.append(stock)
    inputs = {
        "function" : "TIME_SERIES_DAILY",
        "symbol" : str(stock),
        "apikey": "KS1FKWJ9GC7F1M5Z",
        "outputsize": "full"
    }
    response = requests.get("https://www.alphavantage.co/query",inputs)
    
    
    soup_df=pd.DataFrame(response.json()['Time Series (Daily)']).T
    soup_df.reset_index(inplace=True)
    
    soup_df_sort=soup_df.sort_values(by=["index"],ignore_index=True)
    cols=soup_df_sort.columns.drop("index")
    df_temp=soup_df_sort[cols].apply(pd.to_numeric)
    df_temp["Date"]=soup_df_sort["index"]
    stockl=[str(stock) for i in df_temp.index]
    df_temp["Stock"]=pd.DataFrame(stockl)
    
    soup_df_sort=df_temp[['Stock','Date','1. open', '2. high', '3. low', '4. close', '5. volume']]
    daily_stock_df=daily_stock_df.append(soup_df_sort, ignore_index=True)
daily_stock_df.reset_index(drop=True, inplace=True)

print(stocks)


#### Rafael Mello API  test area #### 

#truque pra abrir o site 
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

url = 'https://www.investing.com/equities/zoom-video-communications-earnings'
response = requests.get(url, headers= headers)
response.content
response.content

soup = BeautifulSoup(response.content, features = "lxml")


earnings = soup.find_all('table', attrs= {'class' : 'genTbl openTbl ecoCalTbl earnings earningsPageTbl'})

stocks= soup.find_all('h1')
stock=stocks[0].get_text(strip=True).split(" ")[-1][1:-1]

#toda a informacao dos balancos trimestrais

rows = earnings[0].find_all('tr', attrs = {'name' : 'instrumentEarningsHistory'})



mega_list = []
for row in rows:
    row_list = []
    for stuff in row.find_all("td"):
        row_list.append(stuff.get_text().replace("/ ", ""))
    mega_list.append(row_list+[stock])
    
df = pd.DataFrame(mega_list)

df=df.rename(columns={0: "Release Date", 1: "Period End", 2: "EPS actual" ,3: "EPS forecast", 4: "Revenue actual", 5: "Revenue forecast", 6: "Stock"})
df=df[['Stock','Release Date', 'Period End', 'EPS actual','EPS forecast', 'Revenue actual','Revenue forecast']]

dict_month={"Jan": "01", "Fev": "02", "Mar":"03",
           "Apr":"04", "May": "05", "Jun":"06",
           "Jul":"07", "Aug":"08","Sep":"09",
           "Oct":"10", "Nov":"11","Dec":"12"}
df["Release Date"]=df["Release Date"].apply(lambda x : x[-4:]+"-"+str(dict_month[x[0:3]])+"-"+x[4:6])
df

#### Plot area #### 

Date1="2020-01-01"
Date2="2020-06-30"

xx=daily_stock_df[(daily_stock_df["Stock"]=="ZM") & (daily_stock_df["Date"]>Date1) & (daily_stock_df["Date"]<Date2)]
xx.reset_index(drop=True, inplace=True)
yy=daily_stock_df[(daily_stock_df["Stock"]=="ZOOM") & (daily_stock_df["Date"]>Date1) & (daily_stock_df["Date"]<Date2)]
yy.reset_index(drop=True, inplace=True)
merged=xx.merge(yy, on="Date")


fig=plt.figure(figsize = (20,5))
#ax = fig.add_subplot(111)
plt.plot(merged["Date"],merged["4. close_x"],'b--') #ZM
plt.plot(merged["Date"],merged["4. close_y"],'r--')

"""ymax = max(merged["4. close_y"])
xpos = (merged["4. close_y"] == int(ymax)).index()
xmax = merged["Date"][xpos]

ax.annotate('local max', xy=(xmax, ymax), xytext=(xmax, ymax+5),
            arrowprops=dict(facecolor='black', shrink=0.05))

ax.set_ylim(0,20)"""

plt.show()


#teste week before and after

df["Release Date"][2]



fig=plt.figure(figsize = (5,5))

xxxx=daily_stock_df[(daily_stock_df["Date"]) == (df["Release Date"][1]) & (daily_stock_df["Stock"] == "ZM")]



