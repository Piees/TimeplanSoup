import requests
import calendar
from bs4 import BeautifulSoup
import re



#URL = "http://timeplan.uia.no/swsuiav/XMLEngine/default.aspx?ModuleByWeek&p1=;IS-213-1;&p2=0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23"
URL = ["http://timeplan.uia.no/swsuiav/XMLEngine/default.aspx?ModuleByWeek&p1=;IS-211-1;&p2=0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23",
		"http://timeplan.uia.no/swsuiav/XMLEngine/default.aspx?ModuleByWeek&p1=;IS-213-1;&p2=0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23"]

def textDateToInt(txtDate):
	for index, item in enumerate(calendar.month_name):
		if item[:3] == txtDate:
			return index


# sort by value of date inside each dict inside
# parent dict
def sortByDate(list):
	'''
	insert list containing hashmaps with a date value
	'''
	fish = [] # temp name
	for i in range(len(list)):
		blue = list[i]
		fish = sorted(list, key=lambda blue: blue["dateVal"])
#		fish.append(sorted(list, key=lambda list: list[i]["dateVal"]))
#	list.sort(key=lambda list: list[1]['dateVal'])
	return fish

multiTr = []

for x in URL:
	response = requests.get(x)

	soup = BeautifulSoup(response.text, 'html.parser')

	tr = soup.find_all('tr')

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

	for x in finalTr:
		multiTr.append(x)


for x in multiTr:
	x['dateVal'] = str(textDateToInt(x['date'][3:])) + x['date'][:2]

multiTr = sortByDate(multiTr)


# print all lectures
def unsortedPrint():
	for i in range(len(multiTr)):
		print ""
		for x in multiTr[i]:
			print x + ":", multiTr[i][x]

# print sorted lectures
def sortedPrint():
	for i in range(len(multiTr)):
		print ""
		print "Date:", multiTr[i]['date']
		print "Day:", multiTr[i]['day']
		print "Time:", multiTr[i]['time']
		print "Course:", multiTr[i]['course']
		print "Room:", multiTr[i]['room']
		print "Teacher:", multiTr[i]['tName']

sortedPrint()
