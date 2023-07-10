import os
import json
import sqlite3

class CreateDatabase:
    def __init__(self) -> None:
        self.fileLocation = None
        self.databaseLocation = None
        self.fileName = "bars_data/bars"
    def create(self,filePath=''):
        filePath = self.fileName+'.json'
        Helpers.formatData(self.fileName)
        connection = sqlite3.connect('adviser/resources/databases/bars.db')
        cursor = connection.cursor()
        cursor.execute('Drop Table Bars')
        cursor.execute('Create Table if not exists Bars (name text ,price text ,rating text  ,location text ,hours text ,website text ,phone text ,review text ,serviceOption text ,accessibility text ,offerings text ,diningOptions text ,amenities text ,atmosphere text ,crowd text ,planning text ,payment text ,highlight text ,description text ,numberOfReviews text ,reviewFilter text )')

        filename = self.fileName+'new.json'
        bars = json.load(open(filename))
        columns = ['name','price','rating','location','hours','website','phone','review','serviceOption','accessibility','offerings','diningOptions','amenities','atmosphere','crowd','planning','payment','highlight','description','numberOfReviews','reviewFilter']
        for row in bars:
            keys= tuple(bars[row][c] for c in columns)
            cursor.execute('insert into Bars values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',keys)
            print(row)  

        connection.commit()
        connection.close()
class Helpers:
    @staticmethod
    def formatData(file):
        defaultValue = '~'
        completeDict = {}
 
        bars = json.load(open(file+'.json'))
        for bar in bars:
            outputdict = {}
            outputdict['name'] =  Helpers.getValue(bar,'name')
            outputdict['price'] = Helpers.getValue(bar,'price') 
            outputdict['rating'] = Helpers.getValue(bar,'rating') 
            outputdict['description'] = Helpers.getValue(bar,'HIGHLIGHT')  
            
            moreinfo =  Helpers.getValue(bar,'moreInfo')  
            outputdict =  Helpers.getMoreInfo(moreinfo,outputdict)
 
            about = Helpers.getValue(bar,'about')
            outputdict['accessibility'] = "~".join(Helpers.getValue(about,'Accessibility'))
            outputdict['serviceOption'] = "~".join(Helpers.getValue(about,'Service options'))
            outputdict['offerings'] = "~".join(Helpers.getValue(about,'Offerings'))
            outputdict['amenities'] = "~".join(Helpers.getValue(about,'Amenities'))
            outputdict['atmosphere'] = "~".join(Helpers.getValue(about,'Atmosphere'))
            outputdict['crowd'] = "~".join(Helpers.getValue(about,'Crowd'))
            outputdict['diningOptions'] = "~".join(Helpers.getValue(about,'Dining options'))
            outputdict['payment'] = "~".join(Helpers.getValue(about,'Payments'))
            outputdict['highlight'] = "~".join(Helpers.getValue(about,'Highlights'))
            outputdict['planning'] = "~".join(Helpers.getValue(about,'Planning'))
            
            reviews = Helpers.getValue(about,'reviews')
            outputdict['numberOfReviews'] = "~".join(Helpers.getValue(reviews,'number of reviews'))
            outputdict['reviewFilter'] = "~".join(Helpers.getValue(reviews,'filters'))
            outputdict['review'] = "~".join(Helpers.getValue(reviews,'review text'))

            completeDict[outputdict['name']]= outputdict
        with open(file+'new.json', 'w') as file:
                json.dump(completeDict, file)
    @staticmethod
    def getPhonenumber(info,outputDict):
        try:
            value = str(int(info.replace(" ", "")))
            outputDict['phone'] = value
            return outputDict
        except:
            return outputDict


    @staticmethod
    def getValue(dictionary,searchTerm):
        defaultValue = '~'
        try:
            value = dictionary.get(searchTerm) 
            if value == None:
                return defaultValue
            else:
                return value
        except:
            return defaultValue
    
    @staticmethod
    def getIndexValue(list,index):
        defaultValue = '~'
        try:
            return list[index]
        except:
            return defaultValue
    @staticmethod
    def getMoreInfo(moreInfo,outputDict):
        defaultValue = '~'
        print(moreInfo)
        for index,info in enumerate(moreInfo):
            if(index == 0):
                outputDict['location'] = info
            elif('.' in info):
                outputDict['website'] = info
            elif(outputDict.get('hours') == None and 'Sunday' in info):                
                outputDict['hours'] = json.dumps(info)
            else:
                outputDict = Helpers.getPhonenumber(info,outputDict)
        if(outputDict.get('location')==None):
            outputDict['location'] = defaultValue
        if(outputDict.get('website')==None):
            outputDict['website'] = defaultValue
        if(outputDict.get('hours')==None):
            outputDict['hours'] = defaultValue
        if(outputDict.get('phone')==None):
            outputDict['phone'] = str(00)
        
        return outputDict

cc = CreateDatabase()
cc.create()