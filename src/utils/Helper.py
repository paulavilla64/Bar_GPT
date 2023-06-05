import json
from configparser import SafeConfigParser
import Constants


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,dataObject):
            return {"name": obj.name, "price": obj.price,"rating":obj.rating}
        return super().default(obj)
class dataObject:
	def __init__(self,name) :
		self.name = name
		self.price = "not available"
		self.rating = "not available"

	def addPrice(self,price):
		self.price = price
	
	def addRating(self,rating):
		self.rating = rating

class MinerConfiguration():
    def __init__(self,parser):
        self.url = parser.get(Constants.MinerConfigurationSection, 'url')
        self.searchQuery = parser.get(Constants.MinerConfigurationSection, 'query')
        self.numberOfSearchPerPage = int(parser.get(Constants.MinerConfigurationSection, 'numberOfSearchPerPage'))
        self.numberOfPagesToSearch = int(parser.get(Constants.MinerConfigurationSection, 'numberOfPagesToSearch'))
        self.outputFileName = parser.get(Constants.MinerConfigurationSection, 'outputFileName')
        self.pageWaitTime = parser.get(Constants.MinerConfigurationSection, 'waitTime')
        self.browserNoShow = True if (parser.get(Constants.MinerConfigurationSection, 'browserNoShow')).lower() == "true" else False
        self.driverLocation = parser.get(Constants.MinerConfigurationSection, 'driverLocation')
        self.googleConfig = GoogleSearchConfig(parser)

class GoogleSearchConfig():
    def __init__(self,parser):
        self.acceptConditionsButtonId = parser.get(Constants.GoogleSearchConfigurationSection,"acceptConditionsButtonId")
        self.searchBarId = parser.get(Constants.GoogleSearchConfigurationSection,"searchBarId")
        self.moreOptionsId = parser.get(Constants.GoogleSearchConfigurationSection,"moreoptionsId")
        self.nextButtonId = parser.get(Constants.GoogleSearchConfigurationSection,"nextButtonId")
        self.nameContainerClass = parser.get(Constants.GoogleSearchConfigurationSection,"nameContainerClass")
        self.nameSpanPath = parser.get(Constants.GoogleSearchConfigurationSection,"nameSpanPath")
        self.ratingContainerClass = parser.get(Constants.GoogleSearchConfigurationSection,"ratingContainerClass")
        self.ratingSpanPath = parser.get(Constants.GoogleSearchConfigurationSection,"ratingSpanPath")
        self.priceContainerClass = parser.get(Constants.GoogleSearchConfigurationSection,"priceContainerClass")
        self.priceSpanPath = parser.get(Constants.GoogleSearchConfigurationSection,"priceSpanPath")
        self.searchElementPath = parser.get(Constants.GoogleSearchConfigurationSection,"searchElementPath")
        
    
def getConfigurations():
    parser = SafeConfigParser()
    parser.read(Constants.ConfigurationFile)
    return MinerConfiguration(parser)
    