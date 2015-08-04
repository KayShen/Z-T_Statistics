import selenium,urllib,urllib2,random,time,os,re
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import time

# dcap=dict(DesiredCapabilities.PHANTOMJS)
# ##choose a browser in your phantomjs
# dcap["phantomjs.page.settings.userAgent"] = (
#     "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5"
# )

driver = webdriver.PhantomJS()
driver.set_window_size(1120,550)
driver.get('http://www.linkedin.com/')
driver.find_element_by_id('login-email').send_keys('lumengqian.lulu@gmail.com')
pw=driver.find_element_by_id('login-password')
ActionChains(driver).click(pw).send_keys('l12386').perform()
driver.find_element_by_name('submit').submit()
driver.save_screenshot("/Users/Kay/Desktop/temp1.png")
print driver.current_url
nav_link = driver.find_elements_by_class_name('nav-link')
time.sleep(10)
ActionChains(driver).click(nav_link[2]).perform()
time.sleep(10)
driver.save_screenshot("/Users/Kay/Desktop/temp.png")
print driver.current_url

# soup=BeautifulSoup(driver.page_source, "lxml")
# a=soup.find_all('h3',attrs={'class':'name'})
# a_length = len(a)
# driver.save_screenshot("/Users/Kay/Desktop/temp.png")
# f = open("/Users/Kay/Desktop/aaa.xml", "w")
# f.write(soup.prettify().encode("UTF-8"))
# f.close()
# draw_down1 = True
# while draw_down1:
# 	counter = 1
# 	draw_down2 = True
# 	while (counter <=4) and (draw_down2 == True):
# 		driver.execute_script('window.scrollBy(0,1000);')
# 		soup=BeautifulSoup(driver.page_source)
# 		a=soup.find_all('h3',attrs={'class':'name'})
# 		a_length_new = len(a)
# 		print a_length_new
# 		if a_length != a_length_new:
# 			a_length = a_length_new
# 			draw_down2 = False
# 		elif counter ==4:
# 			draw_down1 = False
# 			print "yes"
# 			print a_length
# 			print a_length_new
# 		counter = counter + 1
# 		print "counter"
# 		print counter
# 		print "draw_down2"
# 		print draw_down2
# 		print "draw_down1"
# 		print draw_down1	
# 		time.sleep(5)
# 	print a_length

# print a_length


