# -*- coding: utf-8 -*-
import requests
import calendar
from bs4 import BeautifulSoup
import re
import sys
import datetime
import urllib2
from seleniumtest import strElements

COURSES = {'is-211': 'Algoritmer og datastrukturer',
			'is-213': 'Åpen kildekode programvare',
			'is-309': 'Videregående databasesystemer',
			'is-113': 'Læring med IT',
			'tfl-119': 'IT og samfunnsendringer',
			'me-108': 'Samfunnsvitenskaplig metode'}

URLDICT = {}

print strElements
for x in strElements:
	URLDICT[x[:-2]] = "http://timeplan.uia.no/swsuiav/XMLEngine/default.aspx?ModuleByWeek&p1=;{};&p2=0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23".format(x)

def textDateToInt(txtDate):
	for index, item in enumerate(calendar.month_name):
		if item[:3] == txtDate:
			if len(str(index)) == 1:
				return "0" + str(index)
			else:
				return str(index)


# sort by value of date inside each dict inside parent dict
def sortByDate(list):
	sort = []
	for i in range(len(list)):
		shortList = list[i]
		sort = sorted(list, key=lambda shortList: shortList["dateVal"])
	return sort

multiTr = []

t = open('textsoup.txt', 'w')
t.truncate()
t.write('[')

i = 1

for x in URLDICT:
	print str(i) + "/" + str(len(URLDICT))
	i += 1

	response = requests.get(URLDICT[x])

	soup = BeautifulSoup(response.text, 'html.parser')

	tr = soup.find_all('tr')

	splitTr = []
	processedTr = []
	finalTr = []
	year = ""

	for x in tr:
		s = str(x).split("<td")
		splitTr.append(s)

	# remove non-class tr
	for x in splitTr:
		for y in x:
			if re.search(".*Uke.*", y) != None:
				year = y[y.index('Uke')+8:y.index('Uke')+12]
				break
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
			temp.append(y.replace("</td>", "").replace("\t", "").replace("\n", "").replace("\r", ""))
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
			dHold["course"] = x[4][2:].split(' ', 1)[0]
			# append room
			dHold["room"] = x[5][1:]
			# append teacher name
			dHold["tName"] = x[6][1:]
			finalTr.append(dHold)
		except:
			pass

	for x in finalTr:
		t.write(str(x) + ',')
t.write(']')
t.close()

for x in multiTr:
	x['dateVal'] = year + str(textDateToInt(x['date'][3:])) + x['date'][:2] + x['time'].split("-")[0].replace(".", "")

multiTr = sortByDate(multiTr)

# return week number
def currentWeek():
	return datetime.datetime.today().isocalendar()[1]

activeWeek = currentWeek()

if __name__ == "__main__":
#    t = open('textsoup.txt', 'w')
#    t.truncate()
#    t.write(str(multiTr))
#    t.close()
    print "Wrote to file"
