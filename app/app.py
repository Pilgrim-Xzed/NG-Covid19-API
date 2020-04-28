import os
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import json
from datetime import date
from urllib.request import urlopen
import re
import time

app = Flask(__name__)

ncdc_url ="https://covid19.ncdc.gov.ng/"

@app.route('/', methods=['GET', 'POST'])
def scrapencdc():
    page = urlopen(ncdc_url)
    soup = BeautifulSoup(page, 'html.parser')
    ncdc_national_data = soup.find('table',{'id':'custom1'})
    ncdc_state_data = soup.find('table',{'id':'custom3'})
    
    data_res_national = {}
    data_res_state = {}
    

    for tr in ncdc_national_data.find_all('tr'):
        tds =tr.find_all('td')
        
        data_res_national[tds[0].text.strip()] =re.sub("\n|>", " ", tds[1].text.strip())

     
        
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
      
    

    return jsonify({"data":{"NCDC_National_Info":data_res_national,"KD_state":data_res_state,"Date":date.today()}})


