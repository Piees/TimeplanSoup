# -*- coding: utf-8 -*-
from flask import Flask, url_for, render_template
#import soup
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
    print x['course']
    for y in selected:
        if x['course'][:-2].lower() == y:
            selCourses.append(x)


def nextLecture():
    switch = False
    today = str(datetime.datetime.today()).replace(' ', '').replace(':', '').replace('.', '').split('-')
    today[2] = today[2][:6]
    for x in selCourses:
        if int(x['dateVal']) >= int(int(today[0] + today[1] + today[2])):
            switch = True
        if switch and (x['dateVal'] != None):
            return x['dateVal']


#def get_resource_as_string(name, charset='utf-8'):
#    with app.open_resource(name) as f:
#        return f.read().decode(charset)


#print "HEI"
#for x in courses:
#    if x['course'] == 'is-211'
#    print x['course']

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
    return render_template('main.html', courses=courses, nextLecture = nextLecture, selected = selected)

if __name__ == '__main__':
#    app.run(debug=False, host="0.0.0.0")
    app.run(debug=True)
