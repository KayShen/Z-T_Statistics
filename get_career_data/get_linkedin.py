import selenium,urllib,urllib2,random,time,os,re
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import time

dcap=dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5"
)

driver = webdriver.PhantomJS()
driver.set_window_size(1120,550)

web_address = 'http://www.linkedin.com/'
email_address = 'lumengqian.lulu@gmail.com'
password = 'l12386'

driver.get('http://www.linkedin.com/')
def log_in(email_address, password):
	driver.find_element_by_id('login-email').send_keys(email_address)
	pw=driver.find_element_by_id('login-password')
	ActionChains(driver).click(pw).send_keys(password).perform()
	driver.find_element_by_name('submit').submit()
	return driver


def go_connection(driver,homepage):
	nav_link = driver.find_elements_by_class_name('nav-link')
	itr = True
	while itr:
		ActionChains(driver).click(nav_link[2]).perform()
		if driver.current_url == homepage:
			time.sleep(5)
		else:
			itr = False
	return driver

def find_contact_count(driver):
	soup=BeautifulSoup(driver.page_source, "lxml")
	contact_count = soup.find_all('span',attrs={'class':'contacts-count'})
	contact_count = int(contact_count[0].strong.string[1:-1])
	print "contact_count: " + str(contact_count)
	return contact_count

def pull_down_page(driver,write_dir):
	soup=BeautifulSoup(driver.page_source, "lxml")
	a=soup.find_all('h3',attrs={'class':'name'})
	a_length = len(a)
	draw_down1 = True
	while draw_down1:
		counter = 1
		draw_down2 = True
		while (counter <=4) and (draw_down2 == True):
			driver.execute_script('window.scrollBy(0,1000);')
			soup=BeautifulSoup(driver.page_source)
			a=soup.find_all('h3',attrs={'class':'name'})
			a_length_new = len(a)
			if a_length != a_length_new:
				a_length = a_length_new
				draw_down2 = False
			elif counter ==4:
				draw_down1 = False
			counter = counter + 1	
			time.sleep(5)
		print "find " + str(a_length) + " connections"
	soup=BeautifulSoup(driver.page_source, "lxml")
	a=soup.find_all('h3',attrs={'class':'name'})
	a_length = len(a)
	f = open(write_dir, "w")
	f.write(soup.prettify().encode("UTF-8"))
	f.close()
	return a_length




driver = log_in(email_address, password)
homepage = driver.current_url
print homepage
driver = go_connection(driver,homepage)
driver.save_screenshot("/Users/Kay/Desktop/temp.png")
connection_page = driver.current_url
print connection_page



contact_count = find_contact_count(driver)
write_dir = "/Users/Kay/Desktop/aaa.xml"
found_contact = pull_down_page(driver,write_dir)






