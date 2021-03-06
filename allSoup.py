# -*- coding: utf-8 -*-
import requests
import calendar
from bs4 import BeautifulSoup
import re
import ast
import sys
import datetime
import urllib2

URLDICT = {}

with open('coursecodes.txt', 'r') as coursecodes:
    coursecodes = coursecodes.read()

coursecodes = ast.literal_eval(coursecodes)

for x in coursecodes:
	URLDICT[coursecodes[x]['strippedCode']] = "http://timeplan.uia.no/swsuiav/XMLEngine/default.aspx?ModuleByWeek&p1=;{};&p2=0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23".format(x)


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

k = 1

for x in URLDICT:
	print str(k) + "/" + str(len(URLDICT))
	k += 1

	response = requests.get(URLDICT[x])

	soup = BeautifulSoup(response.text, 'html.parser')

	tr = soup.find_all('tr')

	splitTr = []
	processedTr = []
	finalTr = []
	year = ""

	for i in tr:
		s = str(i).split("<td")
		splitTr.append(s)

	# remove non-class tr
	if year == "":
		for i in splitTr:
			for y in i:
				if re.search(".*Uke.*", y) != None:
					year = y[y.index('Uke')+8:y.index('Uke')+12]
					break
#			if (len(i) != 8):
#				splitTr.remove(i)

	# remove non-class tr not removed due to
	# in-loop indexerror
#	for i in splitTr:
#		if (len(i) != 8):
#			splitTr.remove(i)

	for i in splitTr:
		temp = []
		for y in i:
			temp.append(y.replace("</td>", "").replace("\t", "").replace("\n", "").replace("\r", ""))
		processedTr.append(temp)

	for y in processedTr:
		if len(y) == 8:
			try:
				dHold = {}
				# append day
				if len(y[1][15:]) == 4:
					dHold["day"] = y[1][15:]
				# append date
				dHold["date"] = y[2][15:]
				# append time
				dHold["time"] = y[3][15:]
				# append course name
				dHold["course"] = x
				# append room
				dHold["room"] = y[5][1:]
				# append teacher name
				dHold["tName"] = y[6][1:]
				# test
#				print year + str(textDateToInt(dHold['date'][3:])) + dHold['date'][:2] + dHold['time'].split("-")[0].replace(".", "")
				dHold['dateVal'] = year + str(textDateToInt(dHold['date'][3:])) + dHold['date'][:2] + dHold['time'].split("-")[0].replace(".", "")
				finalTr.append(dHold)
			except:
				print "except"

	for x in finalTr:
		t.write(str(x) + ',')
t.write(']')
t.close()

with open('textsoup.txt', 'r') as courses:
    courses = courses.read()

courses = ast.literal_eval(courses)

#for x in courses:
#	x['dateVal'] = year + str(textDateToInt(x['date'][3:])) + x['date'][:2] + x['time'].split("-")[0].replace(".", "")

t = open('textsoup.txt', 'w')
t.truncate()

# courses
t.write(str(sortByDate(courses)))

# return week number
def currentWeek():
	return datetime.datetime.today().isocalendar()[1]

activeWeek = currentWeek()

if __name__ == "__main__":
    print "Wrote to file"
