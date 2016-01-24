# -*- coding: utf-8 -*-
from flask import Flask, url_for, render_template
# string to dict module
import ast
import datetime

app = Flask(__name__)

with open('textsoup.txt', 'r') as courses:
    courses = courses.read()

courses = ast.literal_eval(courses)

selected = ['is-213', 'is-211', 'is-110', 'is-202']

selCourses = []

for x in courses:
    for y in selected:
        if x['course'].lower() == y:
            selCourses.append(x)


def nextLecture():
    switch = False
    today = str(datetime.datetime.today()).replace(' ', '').replace(':', '').replace('.', '').split('-')
    today[2] = today[2][:6]
    for x in selCourses:
        print x['dateVal']
        print int(today[0] + today[1] + today[2])
        if int(x['dateVal']) >= int(int(today[0] + today[1] + today[2])):
            switch = True
        if switch and (x['dateVal'] != None):
            return x['dateVal']


# timeplan div
def timeplanDiv():
    div = ""
    for x in courses:
        temp = "<tr><td id=\"highlight\">" + str(x['day']) + "</td><td>" + str(x['date'])
        temp += "</td><td>" + str(x['time']) + "</td><td>" + str(x['course'])
        temp += "</td><td>" + str(x['room'])[:15] + "</td><td>" + str(x['tName'])
        div += temp
    return div


@app.route('/')
def home():
    return render_template('main.html', selCourses=selCourses, nextLecture = nextLecture, selected = selected)

if __name__ == '__main__':
#    app.run(debug=False, host="0.0.0.0")
    app.run(debug=True)
