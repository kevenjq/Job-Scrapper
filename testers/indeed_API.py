"""
import requests

url = "https://indeed-indeed.p.rapidapi.com/apisearch"

querystring = {"publisher":"<REQUIRED>","v":"2","format":"json","callback":"<REQUIRED>","q":"java","l":"austin, tx","sort":"<REQUIRED>","radius":"25","st":"<REQUIRED>","jt":"<REQUIRED>","start":"<REQUIRED>","limit":"<REQUIRED>","fromage":"<REQUIRED>","highlight":"<REQUIRED>","filter":"<REQUIRED>","latlong":"<REQUIRED>","co":"<REQUIRED>","chnl":"<REQUIRED>","userip":"<REQUIRED>","useragent":"<REQUIRED>"}

headers = {
	"X-RapidAPI-Key": "d468097522mshf4e9cf0854b2fb1p1dcc2fjsn0a3fb566a3e0",
	"X-RapidAPI-Host": "indeed-indeed.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
"""

import requests

url = "https://indeed-indeed.p.rapidapi.com/apigetjobs"

querystring = {"publisher": "9084578478905768", "jobkeys": "python", "v": "2", "format": "json"}

headers = {
    "X-RapidAPI-Key": "d468097522mshf4e9cf0854b2fb1p1dcc2fjsn0a3fb566a3e0",
    "X-RapidAPI-Host": "indeed-indeed.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
