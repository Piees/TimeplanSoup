# -*- coding: utf-8 -*-
from flask import Flask, url_for, render_template, request, make_response, redirect
# string to dict module
import ast
import datetime

app = Flask(__name__)

with open('textsoup.txt', 'r') as courses:
    courses = courses.read()

courses = ast.literal_eval(courses)

selected = []

selCourses = []

def updateCourses():
    global selCourses
    selCourses = []
    try:
        for x in courses:
            for y in selected:
                if x['course'].lower() == y:
                    selCourses.append(x)
    except:
        pass
#updateCourses()

def nextLecture():
    switch = False
    today = str(datetime.datetime.today()).replace(' ', '').replace(':', '').replace('.', '').split('-')
    today[2] = today[2][:6]
    for x in selCourses:
#        print x['dateVal']
#        print 'today',int(today[0] + today[1] + today[2])
        if int(x['dateVal']) >= int(int(today[0] + today[1] + today[2])):
            switch = True
        if switch and (x['dateVal'] != None):
#            print x['dateVal']
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


@app.route('/', methods=['POST', 'GET'])
def home():
    global nextLectureVar
    global selected
    selected = []
    selected.append(request.cookies.get('cookieCourse'))
    updateCourses()
    if request.method == 'POST':
        resp = make_response(redirect(url_for('home')))
        if len(request.form['activeCourses']) > 0:
            global selected
            selected = []
            resp.set_cookie('cookieCourse', request.form['activeCourses'] + '#')
            selected.append(request.form['activeCourses'])
        updateCourses()
        return resp
    if request.method == 'GET':
        global selected
        selected = []
        selected.append(request.cookies.get('cookieCourse'))
        updateCourses()
    nextLectureVar = nextLecture()
    return render_template('main.html', selCourses=selCourses, nextLecture = nextLectureVar, selected = request.cookies.get('cookieCourse'))

if __name__ == '__main__':
#    app.run(debug=False, host="0.0.0.0")
    app.run(debug=True)
