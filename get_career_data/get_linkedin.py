import selenium,urllib,urllib2,random,time,os,re
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import time

os.chdir("/Volumes/Data/data")

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
	soup=BeautifulSoup(driver.page_source, "lxml")
	a=soup.find_all('h3',attrs={'class':'name'})
	return len(a)

def click_connection(driver, connection_name, k):
	all_con = driver.find_elements_by_xpath("//a[contains(text(),\""+ connection_name + "\")]")[k].click()
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


name_list = get_name_list(driver)


# homepage = driver.current_url
# print homepage
# driver = go_connection(driver,homepage)
# connection_page = driver.current_url
# print connection_page
driver.save_screenshot("temp.png")

# def get_xml(driver, name_list, homepage, connection_page, k):
for i in range(len(name_list))[142:]:
	try:
		driver.get(connection_page)
	except Exception as e:
		(driver, homepage, connection_page) = reload_page()
		driver.get(connection_page)
	time.sleep(3)
	driver = search_connection(driver,name_list[i].decode("UTF-8"))
	time.sleep(3)
	n_same_connection = find_same_name_connection_number(driver)
	same_name_page = driver.current_url
	print n_same_connection
	print i
	for j in range(n_same_connection):
		time.sleep(3)
		print "opening " + name_list[i] + " homepage"
		driver.get(same_name_page)
		time.sleep(3)
		driver = click_connection(driver, name_list[i].decode("UTF-8"),j)
		time.sleep(3)
		try:
			driver = click_contact_info(driver)
		except Exception as e:
			(driver, homepage, connection_page) = reload_page()
			driver.get(connection_page)
			time.sleep(3)
			driver = search_connection(driver,name_list[i].decode("UTF-8"))
			time.sleep(3)
			same_name_page = driver.current_url
			driver = click_connection(driver, name_list[i].decode("UTF-8"),j)
			time.sleep(3)
			driver = click_contact_info(driver)
		time.sleep(3)
		public_url = find_public_url(driver).encode("UTF-8")
		soup=BeautifulSoup(driver.page_source, "lxml")
		write_dir = "linkedin/" + re.sub("/", "|", str(public_url[29:])) + ".xml"
		f = open(write_dir, "wb")
		f.write(soup.prettify().encode("UTF-8"))
		f.close()
		driver.save_screenshot("linkedin_pic/" + re.sub("/", "|", str(public_url[29:])) + ".png")
		print "xml saved"

