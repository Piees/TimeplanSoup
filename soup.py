import requests
from bs4 import BeautifulSoup
import re



URL = "http://timeplan.uia.no/swsuiav/XMLEngine/default.aspx?ModuleByWeek&p1=;IS-213-1;&p2=0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23"

response = requests.get(URL)

soup = BeautifulSoup(response.text, 'html.parser')

tr = soup.find_all('tr')

def testSplitTr():
	print " "
	print "splitTr 0"
	for x in splitTr[0]:
		print x

	print " "
	print "splitTr 1"
	for x in splitTr[1]:
		print x

	print " "
	print "splitTr 2"
	for x in splitTr[2]:
		print x

	print " "
	print "splitTr 3"
	for x in splitTr[3]:
		print x

def textDateToInt(txtDate):
	for index, item in enumerate(calendar.month_name):
		if item == txtDate:
			return index


splitTr = []
processedTr = []
finalTr = []

for x in tr:
	s = str(x).split("<td")
	splitTr.append(s)
		#splitTr.append(x.split("<td>"))


# remove non-class tr
for x in splitTr:
	if (len(x) != 8):
		splitTr.remove(x)

# remove non-class tr not removed due to
# in-loop indexerror
for x in splitTr:
	if (len(x) != 8):
		splitTr.remove(x)

for x in splitTr:
	temp = []
	for y in x:
		temp.append(y.replace("</td>", ""))
	processedTr.append(temp)

for x in processedTr:
	try:
		dHold = {}
		# append day
		dHold.append(x[1][15:])
		# append date
		dHold.append(x[2][15:])
		# append time
		dHold.append(x[3][15:])
		# append course name
		dHold.append(x[4][3:])
		# append teacher name
		dHold.append(x[5][1:])
		finalTr.append(dHold)
	except:
		pass

#testSplitTr()

for x in finalTr[3]:
	print x
