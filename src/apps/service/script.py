#DOC
#https://github.com/raiak82/dynamicOptionChainPosition

# Libraries
import requests
import json
import math
import os
import json
import pandas as pd
import quantsbin.derivativepricing as qbdp
from datetime import date

DIV_YIELD=0.0344 # RBI Dividend yield


# Python program to print
# colored text and background
def strRed(skk):         return "\033[91m {}\033[00m".format(skk)
def strGreen(skk):       return "\033[92m {}\033[00m".format(skk)
def strYellow(skk):      return "\033[93m {}\033[00m".format(skk)
def strLightPurple(skk): return "\033[94m {}\033[00m".format(skk)
def strPurple(skk):      return "\033[95m {}\033[00m".format(skk)
def strCyan(skk):        return "\033[96m {}\033[00m".format(skk)
def strLightGray(skk):   return "\033[97m {}\033[00m".format(skk)
def strBlack(skk):       return "\033[98m {}\033[00m".format(skk)
def strBold(skk):        return "\033[1m {}\033[0m".format(skk)

# Method to get nearest strikes
def round_nearest(x,num=50): return int(math.ceil(float(x)/num)*num)
def nearest_strike_bnf(x): return round_nearest(x,100)


# Urls for fetching Data
url_oc      = "https://www.nseindia.com/option-chain"
url_bnf     = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
url_indices = "https://www.nseindia.com/api/allIndices"

# Headers
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'accept-language': 'en,gu;q=0.9,hi;q=0.8',
            'accept-encoding': 'gzip, deflate, br'}

sess = requests.Session()
cookies = dict()

# Local methods
def set_cookie():
    request = sess.get(url_oc, headers=headers, timeout=5)
    cookies = dict(request.cookies)

def get_data(url):
    set_cookie()
    response = sess.get(url, headers=headers, timeout=5, cookies=cookies)
    if(response.status_code==401):
        set_cookie()
        response = sess.get(url_nf, headers=headers, timeout=5, cookies=cookies)
    if(response.status_code==200):
        return response.text
    return ""

def set_header():
    global bnf_ul
    global bnf_nearest

    
    # if is_cache_exists():
    #   response_text = get_cache_data()
    # else:
    #   response_text = get_data(bnf_ul)
    #   #do cache
    #   put_cache_data(response_text)

    # response_text = get_data(url_indices)

    # data = json.loads(response_text)
    
    bnf_ul = 38985.95

    # for index in data["data"]:
    #     if index["index"]=="NIFTY BANK":
    #         bnf_ul = index["last"]
    # print("hello ---> ", bnf_ul)

    bnf_nearest=nearest_strike_bnf(bnf_ul)
    return bnf_nearest

# Finding highest Open Interest of People's in CE based on CE data         
def highest_oi_CE(num,step,nearest,url):
    strike = nearest - (step*num)
    start_strike = nearest - (step*num)
    response_text = get_data(url)
    data = json.loads(response_text)
    currExpiryDate = data["records"]["expiryDates"][0]
    max_oi = 0
    max_oi_strike = 0
    for item in data['records']['data']:
        if item["expiryDate"] == currExpiryDate:
            if item["strikePrice"] == strike and item["strikePrice"] < start_strike+(step*num*2):
                if item["CE"]["openInterest"] > max_oi:
                    max_oi = item["CE"]["openInterest"]
                    max_oi_strike = item["strikePrice"]
                strike = strike + step
    return max_oi_strike

# Finding highest Open Interest of People's in PE based on PE data 
def highest_oi_PE(num,step,nearest,url):
    strike = nearest - (step*num)
    start_strike = nearest - (step*num)
    response_text = get_data(url)
    data = json.loads(response_text)
    currExpiryDate = data["records"]["expiryDates"][0]
    max_oi = 0
    max_oi_strike = 0
    for item in data['records']['data']:
        if item["expiryDate"] == currExpiryDate:
            if item["strikePrice"] == strike and item["strikePrice"] < start_strike+(step*num*2):
                if item["PE"]["openInterest"] > max_oi:
                    max_oi = item["PE"]["openInterest"]
                    max_oi_strike = item["strikePrice"]
                strike = strike + step
    return max_oi_strike

# Showing Header in structured format with Last Price and Nearest Strike
def print_header(index="",ul=0,nearest=0):
    print(strPurple( index.ljust(12," ") + " => ")+ strLightPurple(" Last Price: ") + strBold(str(ul)) + strLightPurple(" Nearest Strike: ") + strBold(str(nearest)))

def print_hr():
    print(strYellow("|".rjust(70,"-")))

def oi_fomrater(d):
  return round((d * 25)/100000, 2)

# Check cache data
def is_cache_exists():
    print("check cache", os.path.isfile("bank_full_oi.json"))
    return os.path.isfile("bank_full_oi.json")

# Get Data from cache
def get_cache_data():
    with open("bank_full_oi.json", "r") as openfile:
      return openfile.read()

#Put data in cache
def put_cache_data(json_object):
    print("put in cache")
    with open("bank_full_oi.json", "w") as outfile:
      outfile.write(json_object)

# Fetching CE and PE data based on Nearest Expiry Date
def generate_oi(num,step,nearest,url):
    strike = nearest - (step*num)
    start_strike = nearest - (step*num)
    
    # response_text = get_cache_data()

    if is_cache_exists():
      response_text = get_cache_data()
    else:
      response_text = get_data(url)
      #do cache
      put_cache_data(response_text)

    data = json.loads(response_text) 
    currExpiryDate = data["records"]["expiryDates"][0]
    
    header_text = ["oi","change_oi","value", "strikePrice","impliedVolatility", "underlyingValue", "expiryDate"]
    df_call = pd.DataFrame(columns=header_text)
    df_put = pd.DataFrame(columns=header_text)
    for item in data['records']['data']:
        if item["expiryDate"] == currExpiryDate:
            if item["strikePrice"] == strike and item["strikePrice"] < start_strike+(step*num*2):
                call_list = [
                        oi_fomrater(item["CE"]["openInterest"]), 
                        oi_fomrater(item["CE"]["changeinOpenInterest"]),
                        item["CE"]["lastPrice"], 
                        item["strikePrice"], 
                        item["CE"]["impliedVolatility"],
                        item["CE"]["underlyingValue"],
                        currExpiryDate
                ]
                df_call = df_call.append(pd.Series(dict(zip(df_call.columns, call_list))), ignore_index=True)

                put_list = [
                        oi_fomrater(item["PE"]["openInterest"]), 
                        oi_fomrater(item["PE"]["changeinOpenInterest"]),
                        item["PE"]["lastPrice"], 
                        item["strikePrice"], 
                        item["PE"]["impliedVolatility"],
                        item["PE"]["underlyingValue"],
                        currExpiryDate
                ]
                df_put = df_put.append(pd.Series(dict(zip(df_put.columns, put_list))), ignore_index=True)
                strike = strike + step
    df_call = calculateOptionGreeks(df_call, "Call", currExpiryDate)
    df_call = df_call.add_prefix("call_")
    df_put = calculateOptionGreeks(df_put, "Put", currExpiryDate)
    df_put = df_put.add_prefix("put_")
    df = pd.concat([df_call, df_put], axis=1, join='inner')
  
    return df



def calculateOptionGreeks (df,option_type,expiryDate):
  df['Delta']=pd.Series(dtype='float64')
  df['Gamma']=pd.Series(dtype='float64')
  df['Theta']=pd.Series(dtype='float64')
  pricing_date=date.today().strftime("%Y%m%d")
  df['expiryDate']= pd.to_datetime(df['expiryDate'])
  for index,val in df.iterrows():
      custdate=val['expiryDate'].strftime("%Y%m%d")
      
      market1_parameters = {'spot0': float(val['underlyingValue'])
                    , 'pricing_date':pricing_date
                    , 'volatility':0.01*float(val['impliedVolatility'])
                    , 'rf_rate':DIV_YIELD
                    , 'yield_div':0.0}

      equity_p1 = qbdp.EqOption(option_type=option_type, strike=float(val['strikePrice']), expiry_date=custdate, expiry_type='European')

      eq1_BSM_market1 = equity_p1.engine(model="BSM", **market1_parameters)
      
      df.at[index,'Delta']=float(eq1_BSM_market1.risk_parameters()['delta'])
      df.at[index,'Gamma']=float(eq1_BSM_market1.risk_parameters()['gamma'])
      df.at[index,'Theta']=float(eq1_BSM_market1.risk_parameters()['theta'])
  return df


def get_option_data():
    # set_header()
    # print('\033')
    # print_hr()
    # print_header("Bank Nifty",bnf_ul,bnf_nearest)
    # print_hr()
    option_chain = generate_oi(15,100,bnf_nearest,url_bnf)
    return option_chain
    # print_hr()


    # Finding Highest OI in Call Option In Bank Nifty
    #bnf_highestoi_CE = highest_oi_CE(10,100,bnf_nearest,url_bnf)

    # Finding Highest OI in Put Option In Bank Nifty
    #bnf_highestoi_PE = highest_oi_PE(10,100,bnf_nearest,url_bnf)


    #print(strPurple(str("Major Support in Bank Nifty:")) + str(bnf_highestoi_CE))
    #print(strPurple(str("Major Resistance in Bank Nifty:")) + str(bnf_highestoi_PE))
