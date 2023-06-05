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

import json

outputData = []
	
def extractInformation(browser,config):
	nameContainer = browser.find_element(By.CLASS_NAME,config.nameContainerClass)
	name = nameContainer.find_element(By.XPATH,config.nameSpanPath)
	data = Helper.dataObject(name.text)
	ratingContainer = browser.find_element(By.CLASS_NAME,config.ratingContainerClass)
	rating = ratingContainer.find_element(By.XPATH,config.ratingSpanPath)
	data.addRating(rating.text)
	extractPriceRating(browser,data,config)
	return data

def extractPriceRating(browser,data,config):
	try:
		priceContainer = browser.find_element(By.CLASS_NAME,config.priceContainerClass)
		price = priceContainer.find_element(By.XPATH,config.priceSpanPath)
		data.addPrice(price.text)
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

	chromedriver = "/Users/karan/Downloads"
	browser = webdriver.Chrome(chromedriver)
	return browser
	options = webdriver.ChromeOptions()
	if(config.browserNoShow):  
		options.add_argument("--headless=new")
	return webdriver.Chrome(executable_path=chromedriver,options=options)


def processElement(browser,i,config):
	searchResult = browser.find_element(By.XPATH, f"{config.searchElementPath}[{i}]")
	searchResult.click()
	processResult(browser,config)


def configureBrowser(config):


	browser = getChromeDriver(config)
	browser.implicitly_wait(config.pageWaitTime)
	return browser

def mineData(browser,config):
	browser.get(config.url)
	# Accept Cookies
	browser.find_element("id",config.googleConfig.acceptConditionsButtonId).click()
	# Search in Search Bar
	searchBox = browser.find_element("id",config.googleConfig.searchBarId)
	searchBox.send_keys(config.searchQuery)
	searchBox.send_keys(Keys.RETURN)
	# More Options    - TBD replace this with "maps" button because sometimes this fails when the page gives no more results button
	browser.find_element("xpath",config.googleConfig.moreOptionsId).click()
	# Process Elements on each Search page
	for page in tqdm(range (0,config.numberOfPagesToSearch,1)):
		for ittr in tqdm(range(2,config.numberOfSearchPerPage,2)):
			try:
				processElement(browser,ittr,config.googleConfig)
			except Exception as ex:
				try:
					processElement(browser,ittr,config.googleConfig)
					print(f"ExceptionRaised: {ex}")
				except Exception as ex2:
					print(f"ExceptionRaised2: {ex2}")
					continue
					raise Exception("some error happened!!") # Handle Error - TBD
		# Next Page
		browser.find_element(By.XPATH,config.googleConfig.nextButtonId).click()

def main():
	config = Helper.getConfigurations()
	browser = configureBrowser(config)
	mineData(browser,config)
	dumpData(outputData,config)

def dumpData(data,config):
	json_string = json.dumps(data,cls=Helper.Encoder)
	with open(config.outputFileName, "w") as f:
		f.write(json_string)

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
		print(name)
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
		namee = browser.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[2]/p/span/span')
		data = namee.text
		print("page loaded")
		print(data)

		for ittr in (range(5,30,3)):
			try:
				container = browser.find_element(By.XPATH,f'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[{ittr}]')
				containerPath = f'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[{ittr}]'
				headingElement = browser.find_element(By.XPATH,f'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[{ittr}]/h2') 
				heading = headingElement.text
				print(heading)
				for itt in (range(1,10,1)):
					try:
						list = browser.find_element(By.XPATH,f'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[{ittr}]/ul/li[{itt}]/span')
						val = list.text
						print(val)
					except:
#						continue
						break
			except:
				break


		# mineData(browser,config)
		# dumpData(outputData,config)

if(__name__ == "__main__"):
	main2()
	main()		  
 