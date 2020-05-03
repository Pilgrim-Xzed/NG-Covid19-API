import os
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from pymongo import MongoClient
from bson import json_util, ObjectId
import json

from datetime import date
from urllib.request import urlopen, Request
import re
import time

app = Flask(__name__)

ncdc_url ="https://covid19.ncdc.gov.ng/"
connect = MongoClient("mongodb+srv://Slammad:Slammad42@cluster0-kdk0i.mongodb.net/kmcacademy?retryWrites=true&w=majority")
# establing connection
try:
   
    print("Connected successfully!!!")
    db = connect['covid19']


    collection = db['stats']
except:
    print("Could not connect to MongoDB")

# connecting or switching to the database


@app.route('/', methods=['GET', 'POST'])
def scrapencdc():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
    req = Request(url=ncdc_url, headers=headers) 
    page = urlopen(req).read() 
    soup = BeautifulSoup(page, 'html.parser')
    confirmed_cases = soup.find('div',{'class':'card bg-c-blue order-card'})
    samples_tested = soup.find('div',{'class':'card newcol order-card'})
    active_cases = soup.find('div',{'class':'card bg-c-yellow order-card'})
    discharged_cases = soup.find('div',{'class':'card bg-c-green order-card'})
    deaths = soup.find('div',{'class':'card bg-c-red order-card'})
    ncdc_state_data = soup.find('table',{'id':'custom1'})
    statt = []
    data_res_national = {}
    data_res_national['date'] = str(date.today())
    data_res_state = []
    
    

   
        
    data_res_national[re.sub("\n|>", " ",  confirmed_cases.find('h6').text)] = re.sub("\n|>|,", "",  confirmed_cases.find('h2').text.strip())
    data_res_national[re.sub("\n|>", " ",  samples_tested.find('h6').text)] =re.sub("\n|>|,", "",  samples_tested.find('h2').text.strip())
    data_res_national[re.sub("\n|>", " ",  active_cases.find('h6').text)] =re.sub("\n|>|,", "",  active_cases.find('h2').text.strip())
    data_res_national[re.sub("\n|>", " ",  discharged_cases.find('h6').text)] =re.sub("\n|>|,", "",  discharged_cases.find('h2').text.strip())
    data_res_national[re.sub("\n|>", " ",  deaths.find('h6').text)] =re.sub("\n|>|,", "", deaths.find('h2').text.strip())
    
    if db.stats.find({"date":str(date.today()),"Confirmed Cases":data_res_national[re.sub("\n|>", " ",  confirmed_cases.find('h6').text)],"Active Cases":  data_res_national[re.sub("\n|>", " ",  active_cases.find('h6').text)]}).count() > 0:
        db.stats.update_one({ "date": str(date.today()) },{"$set":json.loads(json_util.dumps(data_res_national))})
    else:
        db.stats.insert_one(json.loads(json_util.dumps(data_res_national)))
    
   
           
            

    statistics = db.stats.find({})
    for item in statistics:
        statt.append(item)

                
            

        
    for tr in ncdc_state_data.find_all('tr'):
        tds = tr.find_all('td')

        if not tr.find_all('th'):
           
                data_res_state .append({
                    "state_name":re.sub("\n|>", " ",  tds[0].string).strip(),
                    "no_of_cases":re.sub("\n|>", " ",  tds[1].string).strip(),
                    "no_of_active_cases":re.sub("\n|>", " ",  tds[2].string).strip(),
                    "no_of_discharged":re.sub("\n|>", " ",  tds[3].string).strip(),
                    "no_of_deaths":re.sub("\n|>", " ",  tds[4].string).strip(),
                })
            
    
      

    return jsonify({"data":{"NCDC_National_Info":data_res_national,"i_by":30,"States":data_res_state,"Hotline":["08035871662","08025088304","08032401473","08037808191"],"Date":date.today(),"item":json.loads(json_util.dumps(statt[::-1]))}})


