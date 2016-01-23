# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()
browser.get('http://www.uia.no/studieplaner/search#tab-to-topics')

for _ in range(2500):
    browser.execute_script("window.scrollBy(0,10000)")

ecode = browser.find_elements_by_xpath("//div[@class='class-topic']/h3/a/span/span/span[@class='attribute-code']")
etitle = browser.find_elements_by_xpath("//div[@class='class-topic']/h3/a/span/span/span[@class='attribute-title']")
eloc = browser.find_elements_by_xpath("//div[@class='class-topic']/h3/a/span/span/span[@class='attribute-location']")
eFullCode = browser.find_elements_by_xpath("//div[@class='class-topic']/h3/a")

codes = {}

for x in range(len(ecode)):
    tempFCode = eFullCode[x].get_attribute('href').split('?')[0]
    tempFCodeFrom = tempFCode.index('topic')+6
    temp = {ecode[x].get_attribute('innerHTML'): {
    'title': etitle[x].get_attribute('innerHTML'),
    'location': eloc[x].get_attribute('innerHTML')[:-5],
    'fullCode': tempFCode[tempFCodeFrom:]
    }}
    codes.update(temp)

for x in codes:
    print x

f = open('coursecodes.txt', 'w')
f.truncate()
f.write(str(codes))
f.close()

browser.close()
