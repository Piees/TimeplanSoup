import requests
from bs4 import BeautifulSoup
import re



#URL = "http://timeplan.uia.no/swsuiav/XMLEngine/default.aspx?ModuleByWeek&p1=;IS-213-1;&p2=0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23"
URL = "http://timeplan.uia.no/swsuiav/XMLEngine/default.aspx?ModuleByWeek&p1=;IS-211-1;&p2=0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23"

response = requests.get(URL)

soup = BeautifulSoup(response.text, 'html.parser')

tr = soup.find_all('tr')


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

#for x in processedTr:
#	print len(x)
#for x in processedTr[0]:
#	print "n"
#	print x


for x in processedTr:
	try:
		dHold = {}
		# append day
		dHold["day"] = x[1][15:]
		# append date
		dHold["date"] = x[2][15:]
		# append time
		dHold["time"] = x[3][15:]
		# append course name
		dHold["course"] = x[4][2:]
		# append room
		dHold["room"] = x[5][1:]
		# append teacher name
		dHold["tName"] = x[6][1:]
		finalTr.append(dHold)
	except:
		pass

#testSplitTr()

#print finalTr[0]

for x in finalTr:
	print x
