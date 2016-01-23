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
#print ecode[0].get_attribute('innerHTML')
#print etitle[0].get_attribute('innerHTML')

codes = []

for x in range(len(ecode)):
    temp = {'code': ecode[x].get_attribute('innerHTML')}
    temp['title'] = etitle[x].get_attribute('innerHTML')
    temp['location'] = eloc[x].get_attribute('innerHTML')[:-5]
    tempFCode = eFullCode[x].get_attribute('href').split('?')[0]
    tempFCodeFrom = tempFCode.index('topic')+6
    temp['fCode'] = tempFCode[tempFCodeFrom:]
    codes += temp

print codes
print ''
print codes[0]

#f = open('coursecodes.txt', 'w')
#f.truncate()
#f.write(str(codes))
#f.close()

browser.close()
