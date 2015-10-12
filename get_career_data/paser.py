import selenium,urllib,urllib2,random,time,os,re
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import time
import re

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
	print homepage
	driver = go_connection(driver,homepage)
	driver.save_screenshot("temp.png")
	connection_page = driver.current_url
	print connection_page
	return (driver, homepage, connection_page)


os.chdir("/Users/Kay/Desktop/lk/")

file_path = os.listdir("first/")
first_connection_list = []
if '.DS_Store' in file_path:
	file_path.remove('.DS_Store')

# item = file_path[90]
# f = open("first/"+item,"r")
# temp = f.read()
# f.close()
# name = re.findall("full-name.*?<\/span>",temp,re.S)[0][41:-25].decode("UTF-8")
# location_part = re.findall("locality\">.*?<\/a>",temp,re.S)[0][13:]
# location = re.findall(">.*?<\/a>",location_part,re.S)[0][22:-24]
# education_part = re.findall("background-education-container.*?<script>",temp,re.S)[0]
# education_part2 = re.findall("<div id.*?<\/div>",education_part,re.S)
# education_sample = education_part2[-1]
# school_name = re.findall("for this school\">.*?</a>",education_sample,re.S)[1][34:-20]
# degree = re.findall("<span class=\"degree.*?<\/span>",education_sample,re.S)[0][38:-24]
# major_part = re.findall("<span class=\"major.*?<\/a>",education_sample,re.S)[0][38:]
# major = re.findall(">.*?<\/a>",major_part,re.S)[0][19:-21]
# try:
# 	start_time = re.findall("<time>.*?<\/time>",education_sample,re.S)[0][22:-22]
# except Exception as e:
# 	start_time = ""

# try:
# 	end_time = re.findall("<time>.*?<\/time>",education_sample,re.S)[1][26:-22]
# except Exception as e:
# 	end_time = ""


for i in range(len(file_path)):
	item = file_path[i]
	for j in range(len(friend_list)):
		webpage = "https://www.linkedin.com/pub/"+re.sub("\|","/",item)[:-4]
		try:
			driver.get(webpage)
			soup = BeautifulSoup(driver.page_source, "lxml")
			if "Sign In" in str(soup):
				(driver, homepage, connection_page) = reload_page()
				driver.get(webpage)
				soup = BeautifulSoup(driver.page_source, "lxml")
		except Exception as e:
			(driver, homepage, connection_page) = reload_page()
			driver.get(webpage)
			soup = BeautifulSoup(driver.page_source, "lxml")

		driver.save_screenshot("temp.png")
		connect_loc = driver.find_element_by_class_name("connections-link")
		ActionChains(driver).click(connect_loc).perform()
		time.sleep(5)
		search_loc = driver.find_elements_by_class_name("search-box standard-form")
		ActionChains(driver).click(search_loc).send_keys(friend_list[j]+"\n").perform()
		time.sleep(5)
		
		# soup = str(BeautifulSoup(driver.page_source, "lxml"))
		# print len(re.findall("<li id=\"connection-.*?<li>",soup,re.S))


