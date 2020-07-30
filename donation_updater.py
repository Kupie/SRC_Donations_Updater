#Change this URL to the URL of the donation page:
url = 'https://www.speedrun.com/mwsf2020/donate'

#How many seconds in between updates. Don't crank this number low, SRC crashes enough as is
timewait = 120

#Check python version
import sys
if sys.version_info < (3, 0):
    sys.stdout.write("Sorry, requires Python 3.x, not Python 2.x\n")
    sys.exit(1)


#Make sure BeautifulSoup is installed
try:
	from bs4 import BeautifulSoup
except ImportError:
    print ('Python module BeautifulSoup not installed, please run "pip install bs4" to install and then run this script again')
    sys.exit(1)

import os
import requests
import time
import ctypes
import urllib3

#sets nice title
ctypes.windll.kernel32.SetConsoleTitleW("Donations Updater")

#disable SSL warnings. SRC requires HTTPS but sometimes their certificate isn't "proper", this makes it connect
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Makes a universal cls function to clear screen. Thanks popcnt: https://stackoverflow.com/a/684344
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

#Plz no bully the SRC servers
#If you're bright enough to remove this, you're bright enough to know we don't need faster than 1 minute updates
if timewait < 60:
	print ('Plz no bullying the SRC servers, 1 minute or more only kthx')
	timewait = 60


#If something contains these strings, then the goal/bidwar is closed 
closedMatching = ["(Goal met!)", "(Closed)"]

#They have set us up the loop
while True:
		
	try:
		#Make the request to SRC, plus the "goals" and "bidwars" page
		rtotal = requests.get(url, verify=False)
		rgoals = requests.get(url + '/goals', verify=False)
		rbids = requests.get(url + '/bidwars', verify=False)
	except:
		#If it fails, URL is invalid... or SRC is down. That's always an option
		print ("Invalid URL connection to SRC failed. Open this python script and check that 2nd line! Exiting...")
		sys.exit(1)
	
	soup = BeautifulSoup(rtotal.content,'html.parser')
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
	
	#Now begins the fucky stuff to update goals
	bidsGoalsText = ''
	soup = BeautifulSoup(rgoals.content,'html.parser')
	div = soup.find('div', class_='panel panel-tabbed')
	#print(div)
	for a in div.find_all('p'):
		#If bidwar/goal contains the closed text, do *not* add it to the main string
		if any(x in a.text for x in closedMatching):
			pass
		else:
			#print (a.text)
			bidsGoalsText += a.text.strip() + ' | '
			
	
	#Let's do bidwars now!
	soup = BeautifulSoup(rbids.content,'html.parser')
	div = soup.find('div', class_='maincontent')
	#print(div)
	for a in div.find_all('p'):
	
		if any(x in a.text for x in closedMatching):
			pass
		else:
			#print (a.text)
			bidsGoalsText += a.text.strip() + ' | '

	#print(bidsGoalsText)
	text_file = open("GoalsBidwars.txt", "w")
	text_file.write(bidsGoalsText)
	text_file.close()


	#Wait "timewait" amount of seconds before running again
	time.sleep(timewait)
	cls()

