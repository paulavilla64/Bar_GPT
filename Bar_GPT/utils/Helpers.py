# import os
# import json
# class Helpers:
#     @staticmethod
#     def formatData(self,filePath):
#         defaultValue = '~'
#         completeDict = {}
# #        filename = '/Users/karan/Downloads/bars.json'
#         bars = json.load(open(filePath))
#         for bar in bars:
#             outputdict = {}
#             outputdict['name'] = (bar.get('name')or defaultValue )
#             outputdict['price'] = (bar.get('price')  or defaultValue  )
#             outputdict['rating'] = (bar.get('rating')  or defaultValue   )
#             outputdict['description'] = (bar.get('HIGHLIGHT')  or defaultValue )  
#             moreinfo = (bar.get('moreInfo')   or defaultValue   )
#             outputdict['location'] = (moreinfo[0]or defaultValue)
#             outputdict['hours'] = (moreinfo[1]or defaultValue)
#             outputdict['website'] = (moreinfo[2]or defaultValue)
#             outputdict['phone'] = self.getPhonenumber(moreinfo)
#             outputdict['accessibility'] = "~".join(bar.get('about').get('Accessibility')or defaultValue)     
#             outputdict['serviceOption'] = "~".join(bar.get('about').get('Service options') or defaultValue )
#             outputdict['offerings'] = "~".join(bar.get('about').get('Offerings') or defaultValue    )
#             outputdict['amenities'] = "~".join(bar.get('about').get('Amenities') or defaultValue   )
#             outputdict['atmosphere'] = "~".join(bar.get('about').get('Atmosphere') or defaultValue  )   
#             outputdict['crowd'] = "~".join(bar.get('about').get('Crowd')   or defaultValue )
#             outputdict['diningOptions'] = "~".join(bar.get('about').get("Dining options")or defaultValue)
#             outputdict['payment'] = "~".join(bar.get('about').get('Payments')  or defaultValue   )
#             outputdict['highlight'] = "~".join(bar.get('about').get('Highlights')or defaultValue)
#             outputdict['numberOfReviews'] = (bar.get('about').get('reviews').get('number of reviews')or defaultValue)
#             outputdict['reviewFilter'] = "~".join(bar.get('about').get('reviews').get('filters') or defaultValue ) 
#             outputdict['review'] = "~".join(bar.get('about').get('reviews').get('review text')or defaultValue)
#             outputdict['planning'] = "~".join(bar.get('about').get('Planning')or defaultValue)
#             completeDict[outputdict['name']]= outputdict
#         with open('/Users/karan/Downloads/barsnew.json', 'w') as file:
#                 json.dump(completeDict, file)
#     @staticmethod
#     def getPhonenumber(self,moreinfoDict:dict):
#         print('getting phone number')
#         try:
#             return str(int(moreinfoDict[3].strip()))
#         except:
#             try:
#                   return str(int(moreinfoDict[4].strip))
#             except:
#                   return str(00)
