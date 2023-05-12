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

TBD
