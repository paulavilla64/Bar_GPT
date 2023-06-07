import os
import json
import sqlite3
#import Bar_GPT.utils.Helpers
#from adviser.Bar_GPT.utils.Helpers import Helpers

class CreateDatabase:
    def __init__(self) -> None:
        self.fileLocation = None
        self.databaseLocation = None
    def create(self,filePath=''):
        filePath = '/Users/karan/Downloads/bars.json'
        Helpers.formatData(filePath=filePath)
        connection = sqlite3.connect('adviser/resources/databases/bars.db')
        cursor = connection.cursor()
        cursor.execute('Create Table if not exists Bars (name text ,price text ,rating text  ,location text ,hours text ,website text ,phone text ,review text ,serviceOption text ,accessibility text ,offerings text ,diningOptions text ,amenities text ,atmosphere text ,crowd text ,planning text ,payment text ,highlight text ,description text ,numberOfReviews text ,reviewFilter text )')

        filename = '/Users/karan/Downloads/barsnew.json'
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
    def formatData(filePath):
        defaultValue = '~'
        completeDict = {}
#        filename = '/Users/karan/Downloads/bars.json'
        bars = json.load(open(filePath))
        for bar in bars:
            outputdict = {}
            outputdict['name'] = (bar.get('name')or defaultValue )
            outputdict['price'] = (bar.get('price')  or defaultValue  )
            outputdict['rating'] = (bar.get('rating')  or defaultValue   )
            outputdict['description'] = (bar.get('HIGHLIGHT')  or defaultValue )  
            moreinfo = (bar.get('moreInfo')   or defaultValue   )
            outputdict['location'] = (moreinfo[0]or defaultValue)
            outputdict['hours'] = (moreinfo[1]or defaultValue)
            outputdict['website'] = (moreinfo[2]or defaultValue)
            outputdict['phone'] = Helpers.getPhonenumber(moreinfo)
            outputdict['accessibility'] = "~".join(bar.get('about').get('Accessibility')or defaultValue)     
            outputdict['serviceOption'] = "~".join(bar.get('about').get('Service options') or defaultValue )
            outputdict['offerings'] = "~".join(bar.get('about').get('Offerings') or defaultValue    )
            outputdict['amenities'] = "~".join(bar.get('about').get('Amenities') or defaultValue   )
            outputdict['atmosphere'] = "~".join(bar.get('about').get('Atmosphere') or defaultValue  )   
            outputdict['crowd'] = "~".join(bar.get('about').get('Crowd')   or defaultValue )
            outputdict['diningOptions'] = "~".join(bar.get('about').get("Dining options")or defaultValue)
            outputdict['payment'] = "~".join(bar.get('about').get('Payments')  or defaultValue   )
            outputdict['highlight'] = "~".join(bar.get('about').get('Highlights')or defaultValue)
            outputdict['numberOfReviews'] = (bar.get('about').get('reviews').get('number of reviews')or defaultValue)
            outputdict['reviewFilter'] = "~".join(bar.get('about').get('reviews').get('filters') or defaultValue ) 
            outputdict['review'] = "~".join(bar.get('about').get('reviews').get('review text')or defaultValue)
            outputdict['planning'] = "~".join(bar.get('about').get('Planning')or defaultValue)
            completeDict[outputdict['name']]= outputdict
        with open('/Users/karan/Downloads/barsnew.json', 'w') as file:
                json.dump(completeDict, file)
    @staticmethod
    def getPhonenumber(moreinfoDict:dict):
        print('getting phone number')
        try:
            return str(int(moreinfoDict[3].strip()))
        except:
            try:
                  return str(int(moreinfoDict[4].strip))
            except:
                  return str(00)

cc = CreateDatabase()
cc.create()