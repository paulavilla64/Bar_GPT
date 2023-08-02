## BarGPT
Spoken Dialogue System Project for Bars in Stuttgart

## Requirements 

- python 3.9+
- run "pip freeze" to get a file with all the required packages. Install all required packages with "pip install <package name>"

## Run

- use command "python run_chat_bars.py bars" to run the code

## Future Work
- Real reservations
- Expanding to multiple domains (restaurants, nightlife clubs, tourist highlights)
- Adaption to different cities



## Dialogue System

## Requestables / Informables
  
Information about Bars

- Enter the name of the bar and ask for:
  - Location
  - Telephone number
  - Opening hours
  - Website
  - Description
  - Price category
  - Rating
  - Reviews from other guests
  - Planning (Accepts/ required reservations)
  - Payment
  - Highlight 
  - Atmosphere
  - Crowd
  - Offerings
  - Dining options
  - Amenities
  - Service option
  - Accessibility


Suggestions about

- Use the keyword "suggest" in your request and ask for bars which offer the following features:
  - Payment (e.g., suggest bars where you can pay with card)
  - Highlight (e.g., suggest bars with live music/ where you can watch sports)
  - Location (e.g., suggest bars around south/ center)
  - Price (e.g., suggest bars which are expensive/ cheap/ average)
  - Rating (e.g., suggest bars with good, bad, average rating)
  - Hours (e.g., suggest bars which are open after midnight)
  - Service option (e.g., suggest bars with outdoor seating, takeaway)
  - Offerings (e.g., suggest bars which serve cocktails, wine)
  - Planning (e.g., suggest bars which require/ accept reservations)
  - Multiple suggestions from different fields (e.g., suggest a bar located around west + good rating + cheap)

Making reservation

- Choose a bar, ask system to make a reservation, enter the desired day and time, system checks if the bar is open, if yes --> reservation is confirmed


