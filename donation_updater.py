#Change this URL to the URL of the donation page:
url = 'https://www.speedrun.com/mwsf2020/donate'

#How many seconds in between updates. Don't crank this number too low, SRC crashes enough as is
timewait = 15

#Should the script iterate through DIVs on the bidwar/goals in revers? (Grabs from the bottom instead of from the top)
#True/False only
ReverseIterate = True

#Manually adjust donations by this much. For example "200" would add 200 to the total at the end
#currently untested, last time it was used this added 50 bucks every update so it needs work lol
Donations_Adjust = 0

#Put the max goals and bids to combine into a string here
maxgoals = 3
maxbids = 3

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

from datetime import datetime
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

#If something contains these strings, then the goal/bidwar is closed 
closedMatching = []
closedMatching = ["(Goal met!)", "(Closed)"]

#initial donations total setting
DonoTotal = '3852'

#They have set us up the loop
while True:
	try:
		#Make the request to SRC, plus the "goals" and "bidwars" page
		rtotal = requests.get(url + '/donations', verify=False)
		rgoals = requests.get(url + '/goals', verify=False)
		rbids = requests.get(url + '/bidwars', verify=False)
	except:
		#If it fails, URL is invalid... or SRC is down. That's always an option
		print ("Invalid URL connection to SRC failed. Open this python script and check that 2nd line! Exiting...")
		sys.exit(1)
	soup = BeautifulSoup(rtotal.content,'html.parser')
	span = soup.find('span', class_='donation-total')
	
	spanint =  int(span.text.replace(',', ''))
	
	if (spanint > int(DonoTotal)):
		DonoTotal = spanint
		DonoTotal = str(int(DonoTotal) + Donations_Adjust)

	
	#Manually adjust donations total from Donations_Adjust value
	
#	Used for testing different number values
#	DonoTotal = '2000'
	if len(DonoTotal) <= 2:
		TotalValue = "   $" + DonoTotal
	elif len(DonoTotal) >= 3:
		TotalValue = "  $" + DonoTotal
	else:
		TotalValue = " $" + DonoTotal
	TotalRaisedText = "Total Raised: $" + DonoTotal
	text_file = open("Totals.txt", "w")
	
	text_file.write(TotalValue)
	text_file.close()
	text_file = open("TotalRaised.txt", "w")
	text_file.write(TotalRaisedText)
	text_file.close()
	
	#Now begins the fucky stuff to update goals
	bidsGoalsText = ''
	soup = BeautifulSoup(rgoals.content,'lxml')
	div = soup.find('div', class_='panel panel-tabbed')
	#print(div)
	dex = 1
	if ReverseIterate:
		divfind = reversed(div.find_all('p'))
	else:
		divfind = div.find_all('p')
		
	for a in divfind:
		#If bidwar/goal contains the closed text, do *not* add it to the main string
		if any(x in a.text for x in closedMatching) or dex > maxgoals:
			pass
		else:
			#print (a.text)
			bidsGoalsText += a.text.strip() + ' | '
			dex += 1
			
	
	#Let's do bidwars now!
	soup = BeautifulSoup(rbids.content,'lxml')
	div = soup.find('div', class_='maincontent')
	#print(div)
	dex = 1
	if ReverseIterate:
		divfind = reversed(div.find_all('p'))
	else:
		divfind = div.find_all('p')
		
	for a in divfind:
	
		if any(x in a.text for x in closedMatching) or dex > maxbids:
			pass
		else:
			#print (a.text)
			bidsGoalsText += a.text.strip() + ' | '
			dex += 1

	text_file = open("GoalsBidwars.txt", "w")
	#This removes unprintable characters, preventing weird shit from showing up
	text_file.write(bidsGoalsText.encode("ascii", errors="ignore").decode())
	text_file.close()

	cls()
	#Doesn't even flash since it's all one "print" command ran immediately
	print('-Marathon URL used:\n--' + url + '\n-' + TotalRaisedText + '\n-Bidwar Text:\n--' + bidsGoalsText + '\n-Last Run at ' + datetime.now().strftime("%I:%M:%S %p") + ', Waiting ' + str(timewait) + ' seconds to run again...')

#	print('Marathon URL used:\n' + url)
#	print (TotalRaisedText)
#	print('Bidwar Text:----\n' + bidsGoalsText)
#	print ('----Last Run at ' + datetime.now().strftime("%I:%M:%S %p") + ', Waiting ' + str(timewait) + ' seconds to run again...')




	#Wait "timewait" amount of seconds before running again
	time.sleep(timewait)
