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
    'port': '3308',
    'database': 'Timeplan'
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
                        tName VARCHAR(64) NULL,
                        dateVal VARCHAR(14) NOT NULL,
                        location VARCHAR(124) NOT NULL,
                        title VARCHAR(164) NOT NULL)''')
        print 'SUCCESSFULLY CREATED TABLE'
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))

def createMoreTables():
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS Date (
                            dates VARCHAR(32) NOT NULL PRIMARY KEY,
                            day VARCHAR(10) NOT NULL
                        );

                        CREATE TABLE IF NOT EXISTS CourseCode (
                            course_id VARCHAR(64) NOT NULL PRIMARY KEY,
                            course_name VARCHAR(64) NOT NULL
                        );

                        CREATE TABLE IF NOT EXISTS Room (
                            room_name VARCHAR(64) NOT NULL PRIMARY KEY
                        );

                        CREATE TABLE IF NOT EXISTS Teacher(
                            teacher_name VARCHAR(128) NOT NULL PRIMARY KEY
                        );


                        CREATE TABLE IF NOT EXISTS Course (
                            date VARCHAR(32) NOT NULL,
                            time TIME NOT NULL,
                            course_id VARCHAR(64) NOT NULL,
                            room VARCHAR(64) NOT NULL,
                            location VARCHAR(64) NOT NULL,
                            teacher VARCHAR(128) NULL,
                            title VARCHAR(64) NOT NULL,
                            PRIMARY KEY(date, course_id),
                            FOREIGN KEY (date) REFERENCES Date(dates),
                            FOREIGN KEY (course_id) REFERENCES CourseCode(course_id),
                            FOREIGN KEY (teacher) REFERENCES Teacher(teacher_name),
                            FOREIGN KEY (room) REFERENCES Room(room_name)
                        );  ''', multi=True)

        print "SUCCESFULLY CREATE THE TABLES"
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))


def remove_non_ascii(text):
    re.sub(r'[^\x00-\x7F]+',' ', text)


createMoreTables()
#createTable()



URLDICT = {}

with open('coursecodes.txt', 'r') as coursecodes:
    coursecodes = coursecodes.read()

coursecodes = ast.literal_eval(coursecodes)

for x in coursecodes:
    coursecodes[x]['URL'] = "http://timeplan.uia.no/swsuiav/XMLEngine/default.aspx?ModuleByWeek&p1=;{};&p2=0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23".format(x)

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

for x in coursecodes:
    print str(k) + "/" + str(len(coursecodes)) + ' ' + str(round(float(k) / len(coursecodes), 4) * 100.00) + '% completed'
    k += 1

    response = requests.get(coursecodes[x]['URL'])

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
            dHold = {}
            # append day
            #if len(y[1][15:]) == 4:
            dHold["day"] = y[1][15:].replace(" ", "")
            # append date
            dHold["dates"] = y[2][15:]
            # append time
            dHold["times"] = y[3][15:]
            # append course name
            dHold["course"] = coursecodes[x]['strippedCode']
            # append room
            dHold["room"] = y[5][1:]
            # append teacher name
            dHold["tName"] = y[6][1:]
            # append date value
            dHold['dateVal'] = year + str(textDateToInt(dHold['dates'][3:])) + dHold['dates'][:2] + dHold['times'].split("-")[0].replace(".", "")
            # append location
            dHold['location'] = coursecodes[x]['location'].replace("&", "")
            # append title
            dHold['title'] = coursecodes[x]['title']

            #for d in dHold:
            #    remove_non_ascii(d)

            exception = False
            errors = []

            try:
                cursor.execute("INSERT INTO Date VALUES (%s, %s)", (dHold['dates'], dHold['day']))
                #cursor.execute("INSERT INTO Date VALUES ('" + dHold['dates'] + "','" + dHold['day'] + "')", multi=True)
                cnect.commit()
            except Exception as e:
                if not type(e) is mysql.connector.IntegrityError:
                    errors.append(type(e).__name__ + " Message: " + e.message)
                    print "Problem with date"
                    exception = True

            try:
                cursor.execute("INSERT INTO CourseCode VALUES (%s, %s)", (dHold['course'], dHold['title']))
                #cursor.execute("INSERT INTO CourseCode VALUES ('" + dHold['course'] + "','" + dHold['title'] + "')", multi=True)
                cnect.commit()
            except mysql.connector.IntegrityError:
                pass
            except Exception as e:
                if not type(e) is mysql.connector.IntegrityError:
                    errors.append(type(e).__name__ + " Message: " + e.message)
                    print "Problem with curse code"
                    exception = True

            try:
                roomValue = { 'room' : dHold['room']}
                #cursor.execute("INSERT INTO Room VALUES ('" + dHold['room'] + "')", multi=True)
                cursor.execute("INSERT INTO Room VALUES (%(room)s)", roomValue)
                cnect.commit()
            except Exception as e:
                if not type(e) is mysql.connector.IntegrityError:
                    errors.append(type(e).__name__ + " Message: " + e.message)
                    print "Problem with Rooom"
                    exception = True

            if dHold["tName"]:
                try:
                    teacherValues = {'teacher_name' : dHold['tName']}
                    #cursor.execute("INSERT INTO Teacher VALUES ('" + dHold['tName'] + "')", multi=True)
                    cursor.execute("INSERT INTO Teacher VALUES (%(teacher_name)s)", teacherValues)
                    cnect.commit()
                except Exception as e:
                    if not type(e) is mysql.connector.IntegrityError:
                        errors.append(type(e).__name__ + " Message: " + e.message)
                        print "Problem with teacher"
                        exception = True

            try:
                if dHold["tName"]:
                    courseValues = {'course_date' : dHold['dates'], 'course_time' : dHold['times'], 'course_id' : dHold['course'], 'room' : dHold['room'], 'location':dHold['location'], 'teacher':dHold['tName'], 'title':dHold['title']}
                    #cursor.execute("INSERT INTO Course VALUES ('" + dHold['dates'] + "','"+ dHold['times'] + "','"+ dHold['course'] + "','"+ dHold['room'] + "','"+ dHold['location'] + "','"+ dHold['tName'] + "','"+ dHold['title']+ "')", multi=True)
                    cursor.execute("INSERT INTO Course VALUES (%(course_date)s, %(course_time)s, %(course_id)s, %(room)s, %(location)s, %(teacher)s, %(title)s )", courseValues)
                    cnect.commit()
                else:
                    courseValues = {'course_date' : dHold['dates'], 'course_time' : dHold['times'], 'course_id' : dHold['course'], 'room' : dHold['room'], 'location':dHold['location'], 'title':dHold['title']}
                    #cursor.execute("INSERT INTO Course VALUES ('" + dHold['dates'] + "','"+ dHold['times'] + "','"+ dHold['course'] + "','"+ dHold['room'] + "','"+ dHold['location'] + "','"+ dHold['title']+ "')", multi=True)
                    cursor.execute("INSERT INTO Course VALUES (%(course_date)s, %(course_time)s, %(course_id)s, %(room)s, %(location)s, %(title)s )", courseValues)
                    cnect.commit()
            except Exception as e:
                print e
                if not type(e) is mysql.connector.IntegrityError:
                    print "Problem with Course"
                    errors.append(type(e).__name__ + " Message: " + e.message)
                    exception = True



            if exception == True:
                print "except" + str(sys.exc_info())
                print dHold['location']
                print dHold['title']
                t.write(str(y) + str(sys.exc_info()) + "\n")

                if len(errors) > 0:
                    for er in errors:
                        print er

cnect.commit()

if __name__ == "__main__":
    print "Created Table and inserted values"
