import selenium,urllib,urllib2,random,time,os,re
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import time
import pickle
import socket
import random

os.chdir("/Users/Kay/Desktop/lk/")

def log_in(driver, email_address, password):
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
			time.sleep(random.random()*2+5)
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
			time.sleep(3)
		print "find " + str(a_length) + " connections"
	soup=BeautifulSoup(driver.page_source, "lxml")
	a=soup.find_all('h3',attrs={'class':'name'})
	a_length = len(a)
	f = open(write_dir, "w")
	f.write(soup.prettify().encode("UTF-8"))
	f.close()
	return a_length

def get_connection_name(driver):
	soup=BeautifulSoup(driver.page_source, "lxml")
	a=soup.find_all('h3',attrs={'class':'name'})
	name_list = []
	for i in range(len(a)):
		print i
		name_list.append(str(a[i].a.string.encode("UTF-8")))
	return name_list

def search_connection(driver,connection_name):
	search_place = driver.find_elements_by_tag_name("input")[8]
	ActionChains(driver).click(search_place).perform()
	search_place2 = driver.find_elements_by_tag_name("input")[8]
	ActionChains(driver).click(search_place2).send_keys(connection_name+"\n").perform()
	return driver

def find_same_name_connection_number(driver):
	a = driver.find_elements_by_xpath("//a[contains(text(),\""+ connection_name + "\")]")
	return len(a)

def click_connection(driver, connection_name, k):
	driver.find_elements_by_xpath("//a[contains(text(),\""+ connection_name + "\")]")[k].click()
	return(driver)

def click_contact_info(driver):
	try:
		driver.find_element_by_id("contacs-tab").click()
	except Exception as e:
		driver.find_element_by_link_text("Contact Info").click()
	return(driver)

def find_public_url(driver):
	public_url_loc = driver.find_element_by_id("relationship-public-profile-link")
	return public_url_loc.text

def get_name_list(driver):
	contact_count = find_contact_count(driver)
	write_dir = "aaa.xml"
	found_contact = pull_down_page(driver,write_dir)
	name_list = get_connection_name(driver)
	return name_list

def reload_page():
	dcap=dict(DesiredCapabilities.PHANTOMJS)
	dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5")
	driver = webdriver.PhantomJS()
	driver.set_window_size(1120,550)
	web_address = 'http://www.linkedin.com/'
	email_address = 'lumengqian.lulu@gmail.com'
	password = 'l12386'
	driver.get('http://www.linkedin.com/')
	driver = log_in(driver, email_address, password)
	homepage = driver.current_url
	# print homepage
	driver = go_connection(driver,homepage)
	driver.save_screenshot("temp.png")
	connection_page = driver.current_url
	# print connection_page
	return (driver, homepage, connection_page)


file_path = os.listdir("first/")
first_connection_list = []
if '.DS_Store' in file_path:
	file_path.remove('.DS_Store')

if '.xml' in file_path:
	file_path.remove('.xml')

# for item in file_path:
# 	item_modified = "https://www.linkedin.com/pub/"+re.sub("\|","/",item)[:-4]
# 	first_connection_list.append(item_modified)
# 	os.makedirs("second_with_people/"+item[:-4])
# 	os.makedirs("second_with_people_pic/"+item[:-4])

socket.setdefaulttimeout(60)
first_connection_url_list = []
for i in range(len(file_path))[2:]:
	print "i = " + str(i)
	item = file_path[i]
	print item
	f = open("first/"+item,"r")
	content = f.read()
	f.close()
	webpage = re.findall("<a class=\"view-public-profile\".*?<\/a>",content,re.S)[0]
	webpage = webpage.split(">")[1][:-4].strip()
	a1=webpage.decode('UTF-8')
	webpage = ''.join([i if not re.search(ur'[\u4e00-\u9fa5]',i) else ''.join(['%'+j.encode('hex') for j in list(i.encode('utf8'))]) for i in list(a1)])
	print webpage
	try:
		driver.get(webpage)
		if "Sign In" in str(soup):
			(driver, homepage, connection_page) = reload_page()
			print "reconnected 1"
			driver.get(webpage)
	except Exception as e:
		(driver, homepage, connection_page) = reload_page()
		print "reconnected 2"
		driver.get(webpage)
	time.sleep(random.random()*2+2)
	print driver.current_url
	driver.save_screenshot("temp.png")
	soup = BeautifulSoup(driver.page_source, "lxml")
	temp = soup.find_all('abbr', attrs = {'aria-hidden':'true'})[0]
	connection_distance = re.findall(r'\d+',str(temp),re.S)[0]
	print "connection distance =  " +connection_distance
	if connection_distance == "1":
		print "mining"
		connect_loc = driver.find_element_by_class_name("connections-link")
		ActionChains(driver).click(connect_loc).perform()
		time.sleep(random.random()*2+5)
		print "connect location clicked"
		driver.save_screenshot("temp.png")
		condition1 = True
		soup = BeautifulSoup(driver.page_source, "lxml")
		if len(soup.find_all('li',attrs = {'class':'nav-all tabs-current'})) == 0:
			condition1 = False
			print "no connection found"
		else:
			print "total connections number"
			total_connection_number = soup.find_all('li',attrs = {'class':'nav-all tabs-current'})[0].string
			print total_connection_number
		friend_list = []
		friend_title_list = []
		counter = 0
		while condition1:
			soup = BeautifulSoup(driver.page_source, "lxml")
			try:
				connection_content = soup.find_all('div',attrs = {'id':'connections'})[0]
				connection_list = connection_content.find_all('a', attrs = {'class':'connections-name'})
				connection_title = connection_content.find_all('p', attrs = {'class':'connections-title'})
				for j in range(len(connection_list)):
					print connection_list[j].string
					print connection_title[j].string
					try:
						friend_list.append(connection_list[j].string.decode("UTF-8"))
					except Exception as e:
						friend_list.append(connection_list[j].string)
					try:
						friend_title_list.append(connection_title[j].string.decode("UTF-8"))
					except Exception as e:
						friend_title_list.append(connection_title[j].string)
			except Exception as e:
				pass
			if len(soup.find_all('button', attrs = {'class':'next carousel-control-disabled'})) == 1:
				next_button = driver.find_element_by_xpath("//button[@class='next carousel-control-disabled']")
				try:
					time.sleep(random.random()*1+1)
					ActionChains(driver).click(next_button).perform()
					time.sleep(random.random()*2+2)
				except Exception as e:
					time.sleep(random.random()*1+3)
					ActionChains(driver).click(next_button).perform()
					time.sleep(random.random()*2+5)
			else:
				condition1 = False
			counter = counter +1
			print "------------- i = " + str(i) + " -------------"
			print "------------- j = " + str(counter) + " -------------"
			print "------------- total connection number = " + str(total_connection_number)
		pickle.dump(friend_list, open("second_with_people/"+item[:-4]+"/friend_list.p", "wb"))
		pickle.dump(friend_title_list, open("second_with_people/"+item[:-4]+"/friend_title_list.p", "wb"))




		# search_loc = driver.find_elements_by_class_name("search-box standard-form")
		# ActionChains(driver).click(search_loc).send_keys(friend_list[j]+"\n").perform()
		# time.sleep(5)





