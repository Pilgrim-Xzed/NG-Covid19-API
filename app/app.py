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
            
    
      

    return jsonify({"data":{"NCDC_National_Info":data_res_national,"i_by":30,"States":data_res_state,"Hotline":[
  {
    "state":"benue",
    "numbers":[
      "09018602439","07025031214","08033696511"
    ]
  },
    {
    "state":"FCT",
    "numbers":[
      "08099936312","08099936313","08099936314","07080631500"
    ]
  },
      {
    "state":"Kogi",
    "numbers":[
      "07088292249","08150953486","08095227003","07043402122"
    ]
  },

    {
    "state":"Kwara",
    "numbers":[
      "09062010001","09062010002"
    ]
  },
   {
    "state":"Nasarawa",
    "numbers":[
      "08036018579","08035871718","08033254549","08036201904","08032910826","08121243191"
    ]
  },
   {
    "state":"Niger",
    "numbers":[
      "08038246018","09093093642","08077213070"
    ]
  },
    {
    "state":"Plateau",
    "numbers":[
      "07032864444","08035422711","08065486416","08035779917"
    ]
  },
   {
    "state":"Adamawa",
    "numbers":[
      "08031230359","07080601139","08115850085","07025040415","09044235334"
    ]
  },
   {
    "state":"Borno",
    "numbers":[
      "08088159881"
    ]
  },
   {
    "state":"Bauchi",
    "numbers":[
      "07088292249","08150953486","08095227003","07043402122"
    ]
  },
   {
    "state":"Gombe",
    "numbers":[
      "08103371257","07026256569","07045257107","07025227843","07026761392","07026799901","07042145504"
    ]
  },
    {
    "state":"Taraba",
    "numbers":[
      "08065508675","08032501165","08039359368","08037450227"
    ]
  },
   {
    "state":"Yobe",
    "numbers":[
      "08131834764","07041116027"
    ]
  },
   {
    "state":"Jigawa",
    "numbers":[
      "08035997118","08036440532","08069323005","08038806682","07035997118","08038629331"
    ]
  },
    {
    "state":"Kaduna",
    "numbers":[
      "08035871662","08025088304","08032401473","08037808191"
    ]
  },
    {
    "state":"Kano",
    "numbers":[
      "08039704476","08037038597","09093995333","09093995444"
    ]
  },
      {
    "state":"Katsina",
    "numbers":[
      "09035037114","09047092428"
    ]
  },
   {
    "state":"Kebbi",
    "numbers":[
      "08036782507","08036074588","08032907601","07035606421","08067677723","08167597029","08083400849","07046352309","07046407663","07046935560"
    ]
  },
    {
    "state":"Sokoto",
    "numbers":[
      "08032311116","08022069567","08035074228","07031935037","08036394462"
    ]
  },
    {
    "state":"Zamfara",
    "numbers":[
      "08035626731","08035161538","08161330774","08065408696","08105009888","08063075385"
    ]
  },
    {
    "state":"Abia",
    "numbers":[
      "07002242362"
    ]
  },
   {
    "state":"Anambra",
    "numbers":[
      "09034728047","09034668319","08163594310","09034663273","09145434416","08117567363"
    ]
  },

    {
    "state":"Ebonyi",
    "numbers":[
      "09020332489","08159279460","07045910340","07085763054"
    ]
  },
  {
    "state":"Enugu",
    "numbers":[
      "08182555550","09022333833"
    ]
  },
   {
    "state":"Imo",
    "numbers":[
      "08099555577","07087110839"
    ]
  },
      {
    "state":"Akwa Ibom",
    "numbers":[
      "08189411111","09045575515","07035211919","08028442194","08037934966","09023330092"
    ]
  },
    {
    "state":"Bayelsa",
    "numbers":[
      "08039216821","07019304970","08151693570"
    ]
  },

      {
    "state":"Rivers",
    "numbers":[
      "09036281412","08031230527"
    ]
  },

    {
    "state":"Delta",
    "numbers":[
      "08033521961","08035078541","08030758179","09065031241"
    ]
  },
    {
    "state":"Edo",
    "numbers":[
      "08084096723","08064258163","08035835529"
    ]
  },

    {
    "state":"Ogun",
    "numbers":[
      "08188978393","08188978392"
    ]
  },

   {
    "state":"Ondo",
    "numbers":[
     
    ]
  },
   {
    "state":"Osun",
    "numbers":[
      "08035025692","08033908772","08056456250"
    ]
  },
   {
    "state":"Oyo",
    "numbers":[
      "08095394000","08095963000","08078288999","08078288800"
    ]
  },
   {
    "state":"Ekiti",
    "numbers":[
      "09062970434","09062970435","09062970436"
    ]
  },
   {
    "state":"Lagos",
    "numbers":[
      "08023169485","08033565529","08052817243","08028971864","08059758886","08035387653"
    ]
  },
],"Date":date.today(),"item":json.loads(json_util.dumps(statt[::-1]))}})


