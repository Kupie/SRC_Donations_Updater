#Change this URL to the URL of the donation page. Ex:
url = 'https://www.speedrun.com/mwsf2020/donate'

#How many seconds in between updates. Don't crank this number low, SRC crashes enough as is
timewait = 60



#Check python version
import sys
if sys.version_info < (3, 0):
    sys.stdout.write("Sorry, requires Python 3.x, not Python 2.x\n")
    sys.exit(1)


#Make sure modules are installed
try:
	from bs4 import BeautifulSoup
	import urllib3
	from lxml import html
except ImportError:
    print ('Required Python modules not installed, please run "pip install lxml bs4" to install and then run this script again')
    sys.exit(1)

import os
import requests
import time

#disable SSL warnings. SRC requires HTTPS but sometimes their certificate isn't "proper", this makes it connect
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Makes a universal cls function to clear screen. Thanks popcnt: https://stackoverflow.com/a/684344
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

#Plz no bully the SRC servers
if timewait < 60:
	print ('Plz no bullying the SRC servers, 1 minute or more only kthx')
	timewait = 60

#They have set us up the loop
while True:
    # Code executed here
		
	try:
		r = requests.get(url, verify=False)
	except:
		print ("Invalid URL. Open this python script and check that 2nd line! Exiting...")
		sys.exit(1)
	
	soup = BeautifulSoup(r.content,'html.parser')
	span = soup.find('span', class_='donation-total')
	
	TotalValue = " $" + span.text
	TotalRaisedText = "Total Raised: $" + span.text
	print (TotalRaisedText)
	print ('Waiting ' + str(timewait) + ' seconds to run again...')
	text_file = open("Totals.txt", "w")
	text_file.write(TotalValue)
	text_file.close()
	text_file = open("TotalRaised.txt", "w")
	text_file.write(TotalRaisedText)
	text_file.close()
	
	#Wait "timewait" amount of seconds before running again
	time.sleep(timewait)
	cls()

