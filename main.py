# -*- coding: utf-8 -*-
from flask import Flask, url_for, render_template
import soup
# string to dict module
import ast
import datetime

app = Flask(__name__)

with open('textsoup.txt', 'r') as courses:
    courses = courses.read()

courses = ast.literal_eval(courses)

# to be deprecated
def sortedPrint():
    fish = []
    dish = ""
    for i in range(len(courses)):
        fish.append(["<br><br>Date:", courses[i]['date'] + "<br>Day:", courses[i]['day'] +
		"<br>Time:", courses[i]['time'] +
		"<br>Course:", courses[i]['course'] +
		"<br>Room:", courses[i]['room'] +
		"<br>Teacher:", courses[i]['tName']])
    for x in fish:
        for i in x:
            dish += i
    return dish

def nextLecture():
    switch = False
    today = str(datetime.datetime.today()).replace(' ', '').replace(':', '').replace('.', '').split('-')
    today[2] = today[2][:6]
    for x in courses:
        if int(x['dateVal']) >= int(int(today[0] + today[1] + today[2])):
            switch = True
        if switch and (x['dateVal'] != None):
            return x


#def get_resource_as_string(name, charset='utf-8'):
#    with app.open_resource(name) as f:
#        return f.read().decode(charset)


# timeplan div
def timeplanDiv():
    div = ""
    for x in courses:
        temp = "<tr><td id=\"highlight\">" + str(x['day']) + "</td><td>" + str(x['date'])
        temp += "</td><td>" + str(x['time']) + "</td><td>" + str(x['course'])
        temp += "</td><td>" + str(x['room'])[:15] + "</td><td>" + str(x['tName'])
        div += temp
    return div

#app.jinja_env.globals['timeplanDiv'] = timeplanDiv

@app.route('/')
def home():
    return render_template('main.html', courses=courses, nextLecture = nextLecture)

if __name__ == '__main__':
    app.run(debug=True)
