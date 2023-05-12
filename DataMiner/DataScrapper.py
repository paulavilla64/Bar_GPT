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
	options = webdriver.ChromeOptions()
	if(config.browserNoShow):  
		options.add_argument("--headless=new")
	return webdriver.Chrome(executable_path=DRIVER_BIN,options=options)


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
			except:
				try:
					processElement(browser,ittr,config.googleConfig)
				except:
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


if(__name__ == "__main__"):
	main()		  
 