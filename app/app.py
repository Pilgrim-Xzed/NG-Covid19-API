import os
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from pymongo import MongoClient
from bson import json_util, ObjectId
import json

from datetime import date
from urllib.request import urlopen
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
    page = urlopen(ncdc_url)
    soup = BeautifulSoup(page, 'html.parser')
    ncdc_national_data = soup.find('table',{'id':'custom1'})
    ncdc_state_data = soup.find('table',{'id':'custom3'})
    
    data_res_national = {}
    data_res_national['date'] = str(date.today())
    data_res_state = {}
    

    for tr in ncdc_national_data.find_all('tr'):
        tds =tr.find_all('td')
        
        data_res_national[tds[0].text.strip()] =re.sub("\n|>", " ", tds[1].text.strip())
        if db.stats.find({"date":str(date.today())}).count() > 0:
            db.stats.update_one({ "date": str(date.today()) },{"$set":json.loads(json_util.dumps(data_res_national))})
        else:
            db.stats.insert_one(json.loads(json_util.dumps(data_res_national)))
    
   
           
            

            
                
            

        
       

        
    for tr in ncdc_state_data.find_all('tr'):
        tds = tr.find_all('td')

        if not tr.find_all('th'):
            if(tds[0].find('p').string == "Kaduna" ):
                data_res_state ={
                    "state_name":tds[0].find('p').string,
                    "no_of_cases":tds[1].find('p').string,
                    "no_of_active_cases":tds[2].find('p').string,
                    "no_of_discharged":tds[3].find('p').string,
                    "no_of_deaths":tds[4].find('p').string
                }
            
    
    

    return jsonify({"data":{"NCDC_National_Info":data_res_national,"KD_state":data_res_state,"Hotline":["08035871662","08025088304","08032401473","08037808191"],"Date":date.today()}})



port = int(os.environ.get("PORT", 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)