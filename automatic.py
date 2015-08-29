# -*- coding: utf-8 -*-
from django.utils.encoding import smart_str
from selenium import webdriver
from bs4 import BeautifulSoup

from selenium.webdriver.common.keys import Keys



keyList  = []
keyFile  = open('./list.txt', 'r')
lines    = keyFile.read().split('\n')
keyFile.close()

for line in lines:
	key = line.split('\t')
	if len(key) == 3:
		keyList.append(key)
		print 'adding  [{0}--{1}--{2}]  to list.'.format( key[2], key[0], key[1]  )

print keyList
# driver = webdriver.Chrome('./chromedriver')
# for i in xrange(5):
	
# 	driver.get("https://google.com/")
	# body = driver.find_element_by_tag_name("body")
	# body.send_keys(Keys.CONTROL + 't')


	# driver.get("https://csrc.edu.tw/")
	# assert u"教育部" in driver.title
	# ID_elem = driver.find_element_by_name("strUserID")
	# PW_elem = driver.find_element_by_name("strPwd")
	# ID_elem.send_keys(userID)
	# PW_elem.send_keys(userPW)
	# PW_elem.send_keys(Keys.RETURN)
	# log        = "/CenterManages/UserData/Edit?user_id=B160001"#+ str(userID)
	# soup       = BeautifulSoup(smart_str(driver.page_source), 'html.parser')
	# table      = soup.find("form", {'id': 'SearchFm', 'name':'SearchFm' })
	# if table == []:
	# 	print 'error'






# driver.close()



# req      = { 'strUserID' : userID, 'strPwd' : userPW }
# response = requests.post( 'https://csrc.edu.tw/', data = req, verify = False )


# soup     = BeautifulSoup(smart_str(response.text))
# table    = soup.find("form", {'id': 'SearchFm', 'name':'SearchFm' })

# for i in table.find_all("td", {'align':'left'}):
# 	link = i.find("a")
# 	if link:
# 		print 'https://csrc.edu.tw' + link['href']

