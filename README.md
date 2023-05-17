# BarGPT
Spoken Dialogue System Project for Bars in Stuttgart

# DataMiner
- Used to scrap data from google maps using Selenium and Chromium Driver

## Bars.json
- This file contains the output from the mining of data

## Requirements 

- python 3.9+
- selenium python package
- chromiumDriver (path to be changed based on Mac or Windows) 

## Run

- Navigate to root folder of the project
- use command "python DataMiner/DataScrapper.py" to run the code

## Bugs
- Sometimes the on running a google search, the search page may not load the button to view more options which can lead upto complete failure of the script
  - can run the script again to fix it 
- Sometimes the loading of the page is super slow which can lead to timeout between scrapping the data from the page resulting in empty results. 
  - good internet connection might help here

## Roadmap
- Need to add more data fields to scrap.
  - Right now gets only the "Name", "Rating" and "Price" for the place


# Dialogue System

## Requestables / Informables
- Can ask at the beginning if you want to stay home or go out
- Stay home options
  - enter ingridents to suggest a recipie
  - occasion
    - work
    - chill
    - date
    - party
  - How many people ?   
- Outing options
  - Type of Drink
  - Special Drink
  - Food Options
  - Rating
  - Ambiance
    - Event
    - Music
    - Cozy
    - Chill
    - Quite
    - Loud
  - Major attraction
  - Type of bar
  - Age Group
  - Distance from location / region of location - south north center east west
  - Location
  - Opening times
  - Website
  - Phone number
  - Rush hour
  - Reviews
