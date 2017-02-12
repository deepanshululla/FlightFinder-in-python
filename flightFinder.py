#!/usr/bin/env python

import requests
import json
from json2html import *
import sys

import smtplib
import time
from html import HTML

reload(sys)
sys.setdefaultencoding('utf-8')
#to have a common format for printing on web page and our terminal

'''
Firstly I appologize for the unclean code.I will be working on it to make it better.
Wrote a script just for myself to keep track of flight prices at different times. The goal was to find a time when flights were cheapest and book them during that time.
It uses Google Flights Rest API to search flights based on their price (first 20 cheapest flights)
then creates a table in HTML and uses that to send and email using SMTP protocol.
To get this working you need to have a key associated with your google APIs account. They will ask for your credit card because they have a tab on the amount of requests each day.
To take care of that I created two keys from my differnt gmail accounts and sent requests to google by loadbalacing the keys.
There is a specific format of Json which needs to be sent which one can see in json1 nested dictionary.

Also you need to enter your email and the email you want to recieve the emails. More imporantly you need to find out your SMTP server.
You don't need to enter your email password(Why? because it is kind of using the insecurity in our email system for a good cause.) 

It also requires installation of following 3rd party python API in your system
--json2html
--html
Their installion is very easily done using pip.
'''

key2='<put your key here>'
key1='<put your second key here>'
 

currentDate=time.strftime("%d/%m/%Y")
currentTime=time.strftime("%H:%M:%S") 

json1={
  "request": {
    "slice": [
      {
        "origin": "BOS",
        "destination": "BOM",
        "date": "2016-12-19"
      },
      {
        "origin": "BOM",
        "destination": "BOS",
        "date": "2017-01-19"
      }
    ],
    "passengers": {
      "adultCount": 1,
      "infantInLapCount": 0,
      "infantInSeatCount": 0,
      "childCount": 0,
      "seniorCount": 0
    },
    "solutions": 50,
    
  }
}
def validateCarrier(str1):
	#simply returns the name of the airline based on their code names
    if "LH" in str1:
        return "Lufthansa"
    elif "UA" in str1:
        return "United Airlines"
    elif "EK" in str1:
        return "Emirates"
    elif "AF" in str1:
        return "Air france"
    elif "LX" in str1:
        return "Swiss"
    elif "BA" in str1:
        return "British Airways"
    elif "CX" in str1:
        return "Cathay Pacific"
    elif "TK" in str1:
        return "Turkish Airlines"
    elif "QR" in str1:
        return "Qatar airways"
    elif "KL" in str1:
        return "KLM Airline company"
    elif "SQ" in str1:
        return "Sinagpore Airlines"
    elif "VS" in str1:
        return "Virgin Atlantic"
    elif "9W" in str1:
        return "Jet Airways"
    else:    
        return "Unknown:"+str1
		
def performSearch(dateBook,url):
    payload['request']['slice'][0]['date']=dateBook
    
    headers = {'content-type': 'application/json','User-Agent': 'Mozilla/5.0'}
    resp = requests.post(url,data=json.dumps(payload), headers=headers)
    jsonResp=resp.json()
    html=json2html.convert(json=jsonResp)
    jsonFile=dateBook+'.json'
    
    f1=open(jsonFile,'w')
    f1.write(json.dumps(jsonResp,indent=4, sort_keys=True))
    f1.close()
    
    jsonFile=dateBook+'.json'
    json_file=open(jsonFile,'r')
    trips = json.load(json_file)
    #print(json_data)
    #trips=json.loads(json_data)
    tripsList=trips['trips']['tripOption']
    sliceArray=tripsList[0]['slice']
    segment=sliceArray[0]['segment']
    #print segment[0]
    h = HTML()
    str1='Flights List leaving '+dateBook+" Current date: "+currentDate+" searched at time "+currentTime
    h.p(str1)
    h.p("")
    t = h.table(border='1')
    r=t.tr;
    r.th("index")
    r.th("id")
    r.th('Flight Cost')
    r.th('departure_duration')
    r.th('departure_carrier')
    r.th('arrival_duration')
    r.th('arrival_carrier')
    r.th("isRefundable")

    for i in range(0,len(tripsList)-1):
        flight=dict()
        flight['cost']=tripsList[i]['saleTotal'].split('USD')[1]
        flight['departure']=dict()
        flight['arrival']=dict()

        flight['departure']['duration']=str(tripsList[i]['slice'][0]['duration']/60)+'H'
        flight['departure']['carrier']=validateCarrier(str(tripsList[i]['slice'][0]['segment'][1]['flight']['carrier']))

        flight['arrival']['duration']=str(tripsList[i]['slice'][1]['duration']/60)+'H'
        flight['arrival']['carrier']=validateCarrier(str(tripsList[i]['slice'][1]['segment'][1]['flight']['carrier']))
        flight['id']=tripsList[i]['id']
        try:
            flight['isRefundable']=str(tripsList[i]['pricing'][0]['refundable'])
        except:
            flight['isRefundable']="False"
        r=t.tr;
        r.td(str(i+1))
        r.td(flight['id'])
        r.td(flight['cost'])
        r.td(flight['departure']['duration'])
        r.td(flight['departure']['carrier'])
        r.td(flight['arrival']['duration'])
        r.td(flight['arrival']['carrier'])
        r.td(flight['isRefundable'])

    htmlFile=dateBook+"_compare.html"    
    f=open(htmlFile,'w+')
    f.write(str(h))
    f.close()
    htmlFile=dateBook+".html"    
    f=open(htmlFile,'w')
    f.write(str(h))
    f.close()
    sender='someEmail@someOrg.com'
    receivers = ['someEmail@someOrg.com','someSecondEmail@someOrg.com']
    message = """From:someEmail@someOrg.com
        To:someEmail@someOrg.com
        Subject: Flight mail
        MIME-Version: 1.0
        Content-type: text/html
        

        """
                            
        
    f=open('htmlFile1.html','r')
    html=f.read()
    f.close()

    message=message+html
    try:
       smtpObj = smtplib.SMTP('<put your smtp server name here>')
       smtpObj.sendmail(sender, receivers, message)         
       print "Successfully sent email"
    except Exception as e:
       print "Error: unable to send email due to "+str(e)
      
    

url1='https://www.googleapis.com/qpxExpress/v1/trips/search?key='
keyArray=[key1,key2]
payload = json1
dateArray=["2016-12-15","2016-12-17","2016-12-18","2016-12-19","2016-12-20","2016-12-21","2016-12-22","2016-12-23","2016-12-24","2016-12-25","2016-12-26","2016-12-27","2016-12-28"]
i=0;
for date in dateArray:
    if i==1:
        i==0
    elif i==0:
        i==1
    url=url1+keyArray[i]    
    performSearch(date,url)
