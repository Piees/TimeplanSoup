# -*- coding: utf-8 -*-
import requests
import calendar
from bs4 import BeautifulSoup
import re
import ast
import sys
import datetime
import urllib2
import mysql.connector
from mysql.connector import errorcode

# Connection details
dbConfig = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'database': 'timeplan'
}

t = open('errorlog.txt', 'w')
t.truncate()

# Connection
cnect = mysql.connector.connect(**dbConfig)

# Cursor
cursor = cnect.cursor()

def createTable():
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS Courses (
                        day VARCHAR(10) NOT NULL,
                        dates VARCHAR(10) NOT NULL,
                        times VARCHAR(14) NOT NULL,
                        course VARCHAR(14) NOT NULL,
                        room VARCHAR(64) NOT NULL,
                        tName VARCHAR(64) NOT NULL,
                        dateVal VARCHAR(14) NOT NULL)''')
        print 'SUCSESFULLY CREATED TABLE'
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        #exit(1)

createTable()

URLDICT = {}

with open('coursecodes.txt', 'r') as coursecodes:
    coursecodes = coursecodes.read()

coursecodes = ast.literal_eval(coursecodes)

for x in coursecodes:
    URLDICT[coursecodes[x]['strippedCode']] = "http://timeplan.uia.no/swsuiav/XMLEngine/default.aspx?ModuleByWeek&p1=;{};&p2=0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23".format(x)

#URLDICT['is-211'] = 'http://timeplan.uia.no/swsuiav/XMLEngine/default.aspx?ModuleByWeek&p1=;IS-211-1;&p2=0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23'

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
                dHold["dates"] = y[2][15:]
                # append time
                dHold["times"] = y[3][15:]
                # append course name
                dHold["course"] = x
                # append room
                dHold["room"] = y[5][1:]
                # append teacher name
                dHold["tName"] = y[6][1:]
                dHold['dateVal'] = year + str(textDateToInt(dHold['dates'][3:])) + dHold['dates'][:2] + dHold['times'].split("-")[0].replace(".", "")
                #cursor.execute("INSERT INTO Courses VALUES ({},{},{},{},{},{},{})".format(dHold['day'], dHold['date'], dHold['time'], dHold['course'],dHold['room'], dHold['tName'], dHold['dateVal']))
                cursor.execute("INSERT INTO Courses VALUES (%(day)s, %(dates)s, %(times)s, %(course)s, %(room)s, %(tName)s, %(dateVal)s)", dHold)
                print 'insert successfull'
            except:# mysql.connector.Error as err:
#                print("Failed creating database: {}".format(err))
                print "except" # + str(sys.exc_info()[0])
                t.write(str(y) + "\n")
#                except mysql.connector.Error as err:
#                    print("Failed creating database: {}".format(err))
#                   exit(1)

cnect.commit()
# return week number
def currentWeek():
    return datetime.datetime.today().isocalendar()[1]

activeWeek = currentWeek()

if __name__ == "__main__":
    print "Wrote to file"
