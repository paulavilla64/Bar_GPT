from configparser import SafeConfigParser
from src.utils.Constants import *
from src.utils.Helper import *


class ConfigManager(metaclass=SingletonMeta):
    def __init__(self):
        parser = self.getParser()
        self.appConfig = AppConfiguration(parser)
        self.mi
        self.dataConfig = DataConfiguration(parser)
        self.openSmileConfig = OpenSmileConfiguration(parser)
        self.librosaConfig = LibrosaConfiguration(parser)
 

    def getParser(self):
        parser = SafeConfigParser()
        parser.read(ConfigurationFile)
        return parser


class AppConfiguration():
    def __init__(self,parser) -> None:
        configSection = parser[AppConfigurationSection]
        self.logFolder = configSection['logFolder']
        self.logFile = configSection['logFile']
        self.logLevel = configSection['logLevel']
        self.performFeatureExtraction = Helper.stringToBool(configSection['performFeatureExtraction'])   

def getConfigurations():
    parser = SafeConfigParser()
    parser.read(Constants.ConfigurationFile)
    return MinerConfiguration(parser)
    
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
        