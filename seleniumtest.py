# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()
browser.get('http://timeplan.uia.no/swsuiav/public/no/default.aspx')
browser.execute_script('__doPostBack(\'LinkBtn_modules\',\'\')')
elements = browser.find_elements_by_xpath("//select[@class='DepartmentFilter']/option")
#for x in elements:
#    print ''
#    print x.get_attribute('innerHTML')
#    f = x.get_attribute('innerHTML').split(' ', 1)[0]
#    print f
strElements = {}
for x in elements:
    temp = x.get_attribute('innerHTML').split(' ', 1)
    if len(temp[0]) > 5:
        if temp[0][1].isupper() and temp[0][len(temp[0])-3].isdigit():
            strElements[temp[0].lower()] = temp[1]
browser.close()

t = open('txtsplit.txt', 'w')
t.truncate()
t.write(str(strElements))

for x in strElements:
    print x
