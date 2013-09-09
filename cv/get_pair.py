import re
import requests
import urllib
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup as bs

from selenium import webdriver
driver = webdriver.Firefox()
#cookie_value = raw_input("cookie> ")
URL = "http://portal.uspto.gov/pair/PublicPair"



#br = mechanize.Browser()
#br.addheaders = [('User-agent', 'Feedfetcher-Google-iGoogleGadgets;\
# (+http://www.google.com/feedfetcher.html)')]
#cj = cookielib.LWPCookieJar()
#br.set_cookiejar(cj)
#br.set_handle_robots(False)
#before = br.open(URL).read()

#cj._cookies['portal.uspto.gov']['/pair']['JSESSIONID'].value = cookie_value
#after = br.open(URL).read()
#print 'Advanced to new page?', before != after
#
#soup = bs(after)
#br.select_form(name="save")
#br.form['dosnum'] = '09/621670'
#before = br.response().read()
#
#data = {'selectedTab': 'ifwtab',
#        'isSubmitted': 'isSubmitted',
#        'public_selectedSearchOption': '',
#        'dosnum': '0921670'}
#data = urllib.urlencode(data)
#br.open(URL, data)
#after = br.response().read()
#print 'Advanced to new page?', before != after

driver.get(URL)
raw_input()
form = driver.find_element_by_id('number_id')
form.send_keys('09/621670')
submitbutton = driver.find_element_by_id('SubmitPAIR')
submitbutton.click()
driver.execute_script("submitTab('ifwtab')")
