import os
from configparser import SafeConfigParser
from src.utils.Constants import *
from  src.utils.Helper import *


# Configure logging

def main():

    initializeApplication()
    controller = KrusaderController()

    controller.start()


def initializeApplication():
    configuration = ConfigManager() 
    if not os.path.exists(configuration.appConfig.logFolder):
        create_folders(configuration.appConfig.logFolder)    
    if not os.path.exists(configuration.openSmileConfig.LLDOutputFolder):
        create_folders(configuration.openSmileConfig.LLDOutputFolder)
    if not os.path.exists(configuration.openSmileConfig.FunctionalsOuputFolder):
        create_folders(configuration.openSmileConfig.FunctionalsOuputFolder)
    if not os.path.exists(configuration.librosaConfig.outputFolder):
        create_folders(configuration.librosaConfig.outputFolder)
    
    krusader_logger = KrusaderLogger().get_logger()


def create_folders(path):
    os.makedirs(path, exist_ok=True)

if __name__ == '__main__':
    main()

