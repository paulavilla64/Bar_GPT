import os
from typing import Any
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import json
from selenium.webdriver.common.by import By
import Helper
from tqdm import tqdm
import time
import json

outputData = []
n_reivews = 50 
 
def processAbout(browser,data):
	try:
		container = find_element(By.CLASS_NAME,'RWPxGd',browser)
		aboutelement = find_element("xpath",'./button[3]',container)
	#	aboutelement = browser.find_element("xpath",'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[3]')
	except:
		aboutelement = find_element("xpath",'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[3]',browser)
	aboutelement.click()
#description
	start = 5
	dict = {}
	# try:
	# 	desc = browser.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[2]')
	# 	dess = desc.browser.find_element('./p/span/span')
	# 	description = desc.text
	# 	print("page loaded")
	# 	dict['description'] = description
	# 	print(description)
	# except Exception as ex:
	# 	print("no description")
	# 	start = 2

	for ittr in (range(2,30,3)):
		try:
			container = find_element(By.XPATH,f'//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]/div[{ittr}]',browser)
			#containerPath = f'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[{ittr}]'
			headingElement = find_element(By.XPATH,f'./h2',container) 
			heading = headingElement.text

			listi = []
#			print(heading)
			for itt in (range(1,10,1)):
				try:
					list = find_element(By.XPATH,f'./ul/li[{itt}]/span',container)
					val = list.accessible_name
#					vall = list.accessible_name
					listi.append(val)
#					print(val)
				except Exception as ex:
					break
			dict[heading] = listi
		except Exception as ex2:
			if(ittr < 3):
				continue
			else:
				break
	data['about'] = dict

def processInfor(browser,data):
#	print('info')
	description = find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[6]/button/div[2]/div[1]/div[1]',browser)
#	print(description.accessible_name)
#	print(description.text)
	data['about']['description'] = description.text
	moreinfo = []
	for itrr in range(3,10,1):
		try:
			ele = find_element(By.XPATH,f'//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[9]/div[{itrr}]',browser)
#			print(ele.text)
			moreinfo.append(ele.text)
		except:
#			print('not found')
			break
	data['about']['moreInfo'] = moreinfo
def find_element(how,path,driver):
	try:
		return driver.find_element(how,path)
	except:
		try:
			return driver.find_element(how,path)
		except Exception as ex: 
			raise(ex)
			try:
				return driver.find_element(how,path)
			except:
				try:
					return driver.find_element(how,path)
				except:
					try:
						return driver.find_element(how,path)
					except Exception as ex:
						raise(ex)

def processReviews(browser,data):
	#print('reviwes')
	reviews = {}
	try:
		container = find_element(By.CLASS_NAME,'RWPxGd',browser)
		reviewelement = find_element("xpath",'./button[2]',container)
	#	aboutelement = browser.find_element("xpath",'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[3]')
	except:
		reviewlement = find_element("xpath",'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[3]',browser)
	reviewelement.click()
	numberOfReviews = find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]/div[1]/div/div[2]/div[2]',browser)
	#print(numberOfReviews.text)
	reviews['number of reviews'] = numberOfReviews.text

	allFilter = []
	reviewFilters = find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]/div[9]',browser)
	for itr in range(1,10,1):
		try:
			reviewFilter = find_element(By.XPATH,f'./div[{itr}]/button/span/span',reviewFilters)
			#print(reviewFilter.text)
			allFilter.append(reviewFilter.text)
		except:
			break
	reviews['filters'] = allFilter

	texts = []
	for itr in range(1,n_reivews,3):
		try:
			reviewTextContainer = find_element(By.XPATH,f'//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]/div[10]/div[{itr}]',browser)
			reviw = find_element(By.XPATH,'./div/div/div[4]/div[2]/div/span[1]',reviewTextContainer)
			#print(reviw.text)
			texts.append(reviw.text)
			
		except Exception as ex:
			break
	reviews['review text'] = texts

	data['about']['reviews'] = reviews

def extractInformation(browser,config):
	config.nameContainerClass = "tAiQdd"
	nameContainer = find_element(By.CLASS_NAME,config.nameContainerClass,browser)
	config.nameSpanPath = './div[1]/div[1]/h1'
	name = find_element(By.XPATH,config.nameSpanPath,nameContainer)
	data = {}
	data['name'] = name.text
	config.ratingContainerClass = 'F7nice'
	ratingContainer = find_element(By.CLASS_NAME,config.ratingContainerClass,browser)
	config.ratingSpanPath = './span[1]/span[1]'
	rating = find_element(By.XPATH,config.ratingSpanPath,ratingContainer)
	data['rating']=(rating.text)
	extractPriceRating(browser,data,config)
	data['about'] = {}
	data['review'] = {}
	processInfor(browser,data)
	processAbout(browser,data)
	processReviews(browser,data)
	return data

def extractPriceRating(browser,data,config):
	try:
		config.priceSpanPath = './span/span[2]/span/span'
		config.priceContainerClass = 'mgr77e'
		priceContainer = find_element(By.CLASS_NAME,config.priceContainerClass,browser)
		price = find_element(By.XPATH,config.priceSpanPath,priceContainer)
		data['price']=(price.text)
	except:
		return

def processResult(browser,config):
	try:
		data = extractInformation(browser,config)
	except:
		data = extractInformation(browser,config)
	outputData.append(data)
   
def getChromeDriver(config):
	PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
	DRIVER_BIN = os.path.join(PROJECT_ROOT, config.driverLocation )

	chromedriver = "..\chromeDriver"
	options = webdriver.ChromeOptions()
	if(config.browserNoShow):  
		options.add_argument("--headless=new")
	browser = webdriver.Chrome(chromedriver,options=options)
	return browser
	options = webdriver.ChromeOptions()
	if(config.browserNoShow):  
		options.add_argument("--headless=new")
	return webdriver.Chrome(executable_path=chromedriver,options=options)


def processElement(browser,i,config):
	searchResult = find_element(By.XPATH, f'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[{i}]/div/a',browser)
	searchResult.click()
	time.sleep(6) # change this
	processResult(browser,config)


def configureBrowser(config):


	browser = getChromeDriver(config)
	browser.implicitly_wait(config.pageWaitTime)
	return browser
def infinite_scroll(driver):
    number_of_elements_found = 0
    while True: 
        els = driver.find_elements(By.CSS_SELECTOR, '.TFQHme')
        if number_of_elements_found == len(els):
            # Reached the end of loadable elements
            break
		
        try:
            driver.execute_script("arguments[0].scrollIntoView();", els[-1])
            number_of_elements_found = len(els)

        except :
            # Possible to get a StaleElementReferenceException. Ignore it and retry.
            pass
def scroll(driver):
	try:
		els = driver.find_elements(By.CSS_SELECTOR, '.TFQHme')
		driver.execute_script("arguments[0].scrollIntoView();", els[-1])
	except:
		pass
def mineData(browser,config):
	browser.get(config.url)
	# Accept Cookies
	browser.find_element("id",config.googleConfig.acceptConditionsButtonId).click()

	#chantge languge
	time.sleep(2)
	eng = browser.find_element("xpath",'//*[@id="SIvCob"]/a')
	eng.click()
	time.sleep(2)
	# Search in Search Bar
	searchBox = browser.find_element("id",config.googleConfig.searchBarId)
	searchBox.send_keys(config.searchQuery)
	time.sleep(2)
	searchBox.send_keys(Keys.RETURN)
	time.sleep(2)
	# More Options    - TBD replace this with "maps" button because sometimes this fails when the page gives no more results button
	#ele = browser.find_element("xpath",'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]')

### language
#	browser.find_element('xpath','//*[@id="Rzn5id"]/div/a[1]').click()
#	time.sleep(5)

	browser.find_element("xpath",config.googleConfig.moreOptionsId).click()
	# Process Elements on each Search page
#	infinite_scroll(browser)
#	for page in tqdm(range (0,config.numberOfPagesToSearch,1)):
	for ittr in tqdm(range(3,config.numberOfSearchPerPage,2)):
		try:			
			processElement(browser,ittr,config.googleConfig)
		except Exception as ex:
			try:
				processElement(browser,ittr,config.googleConfig)
				#print(f"ExceptionRaised: {ex}")
			except Exception as ex2:
				#print(f"ExceptionRaised2: {ex2}")
				continue
				raise Exception("some error happened!!") # Handle Error - TBD
		# Next Page
		if(ittr%5 ==0):
			scroll(browser)
		#browser.find_element(By.XPATH,config.googleConfig.nextButtonId).click()

def main():
	config = Helper.getConfigurations()
	browser = configureBrowser(config)
	
	try:
		mineData(browser,config)
	except Exception as ex:
		print(ex)
	dumpData(outputData,config)

def dumpData(data,config):
#	json_string = json.dumps(data,cls=Helper.Encoder)
	with open(config.outputFileName, 'w') as file:
        	json.dump(data, file)
def main2():
	datas = []
	with open('bars.json', 'r') as f:
		datas = json.load(f)
	config = Helper.getConfigurations()
	browser = configureBrowser(config)
	config.url = 'https://www.google.com/maps?output=classic'
	config.googleConfig.acceptConditionsButtonId = '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button'
	browser.get(config.url)
	# Accept Cookies
	browser.find_element("xpath",config.googleConfig.acceptConditionsButtonId).click()
	config.googleConfig.searchBarId = 'searchboxinput'
	for entry in datas:
		name = entry['name']
		#print(name)
		# perform search
		config.searchQuery = name + " bar Stuttgart"
		# Search in Search Bar
		searchBox = browser.find_element("id",config.googleConfig.searchBarId)
		searchBox.send_keys(config.searchQuery)
		searchBox.send_keys(Keys.RETURN)
		# More Options    - TBD replace this with "maps" button because sometimes this fails when the page gives no more results button
#		browser.find_element("xpath",config.googleConfig.moreOptionsId).click()

# about
		browser.find_element("xpath",'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[3]').click()
#description
		try:
			desc = browser.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[2]/p/span/span')
			description = desc.text
			#print("page loaded")
			#print(description)
		except Exception as ex:
			print("no description")

		for ittr in (range(5,30,3)):
			try:
				container = browser.find_element(By.XPATH,f'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[{ittr}]')
				containerPath = f'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[{ittr}]'
				headingElement = browser.find_element(By.XPATH,f'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[{ittr}]/h2') 
				heading = headingElement.text
				#print(heading)
				for itt in (range(1,10,1)):
					try:
						list = browser.find_element(By.XPATH,f'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[{ittr}]/ul/li[{itt}]/span')
						val = list.text
						#print(val)
					except:
#						continue
						break
			except:
				break


		# mineData(browser,config)
		# dumpData(outputData,config)

if(__name__ == "__main__"):
#	main2()
	main()		  
 