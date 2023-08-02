from services.service import PublishSubscribe
from utils import SysAct, SysActionType
from utils.beliefstate import BeliefState
from services.policy.policy_handcrafted import HandcraftedPolicy
from utils.useract import UserActionType
import json
import dateparser
from datetime import datetime, timedelta
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import wordnet
from nltk.collocations import BigramCollocationFinder
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import requests
import re

class Policy(HandcraftedPolicy):
    def __init__(self, domain, logger, max_turns):
        super().__init__(domain, logger, max_turns)
        """
        Initializes the policy
        """

    
    @PublishSubscribe(sub_topics=["beliefstate"], pub_topics=["sys_act", "sys_state"])
    def choose_sys_act(self, beliefstate: BeliefState) -> dict(sys_act=SysAct):
        """
        Responsible for walking the policy through a single turn. Uses the current user
        action and system belief state to determine what the next system action should be.

        To implement an alternate policy, this method may need to be overwritten

        Args:
            belief_state (BeliefState): a BeliefState obejct representing current system knowledge

        Returns:
            (dict): a dictionary with the key "sys_act" and the value that of the systems next action
        """
        
        self.turns += 1
        # do nothing on the first turn --LV
        sys_state = {}
        if self.first_turn and not beliefstate['user_acts']:
            self.first_turn = False
            sys_act = SysAct()
            sys_act.type = SysActionType.Welcome
            sys_state["last_act"] = sys_act
            return {'sys_act': sys_act, "sys_state": sys_state}

        # Handles case where it was the first turn, but there are user acts
        elif self.first_turn:
            self.first_turn = False

        if self.turns >= self.max_turns:
            sys_act = SysAct()
            sys_act.type = SysActionType.Bye
            sys_state["last_act"] = sys_act
            return {'sys_act': sys_act, "sys_state": sys_state}

        # removes hello and thanks if there are 5also domain specific actions
        self._remove_gen_actions(beliefstate)
        if UserActionType.Bad in beliefstate["user_acts"]:
            sys_act = SysAct()
            sys_act.type = SysActionType.Bad
        # if the action is 'bye' tell system to end dialog
        elif UserActionType.Bye in beliefstate["user_acts"]:
            sys_act = SysAct()
            sys_act.type = SysActionType.Bye
        # if user only says thanks, ask if they want anything else
        elif UserActionType.Thanks in beliefstate["user_acts"]:
            sys_act = SysAct()
            sys_act.type = SysActionType.RequestMore
        # If user only says hello, request a random slot to move dialog along
        elif UserActionType.Hello in beliefstate["user_acts"] or UserActionType.SelectDomain in beliefstate["user_acts"]:
            # as long as there are open slots, choose one randomly
            if self._get_open_slot(beliefstate):
                sys_act = SysAct()
                sys_act.type = SysActionType.Request
                slot = self._get_open_slot(beliefstate)
                sys_act.add_value(slot)

            # If there are no more open slots, ask the user if you can help with anything else since
            # this can only happen in the case an offer has already been made --LV
            else:
                sys_act = SysAct()
                sys_act.type = SysActionType.RequestMore

            # If we switch to the domain, start a new dialog
            if UserActionType.SelectDomain in beliefstate["user_acts"]:
                self.dialog_start()
            self.first_turn = False

            # handle make a reservation user act
        elif UserActionType.MakeReservation in beliefstate["user_acts"]:
            sys_act = SysAct()
            sys_act.type = SysActionType.MakeReservation  # @karan - change this name to system asking for reservation / reservatiion mode

        elif UserActionType.Suggestion in beliefstate["user_acts"]:
            try:
                user_query = beliefstate['reservation_query']
                suggestion_query = Policy.tokenize_sentence(user_query)
                suggestion_slots = set(beliefstate['suggestion_slot'].split("~"))
                suggestion_slots.discard("diningOptions")
                
                if("payment" in suggestion_slots):
                    suggestion_slots.discard("planning")
                    suggestion_slots.discard("accessibility")
                suggestion_slots.discard("")
                suggestion_slots.discard(" ")
                beliefstate['informs'] = {}
                db_data = self._query_db(beliefstate)
                bar_names = set()
                list_of_suggested_bars = []
                
                if('near' in user_query or 'around' in user_query):
                    near_by_bars = Policy.filter_by_region(user_query,db_data)
                    list_of_suggested_bars.append(near_by_bars)
                for suggestion_slot in suggestion_slots:
                    suggested_bar_names_for_slots = set()
                    for bar_data in db_data:
                        for query_element in suggestion_query:
                            if(suggestion_slot == 'price'):
                                if(Policy.check_price_rating(query_element,bar_data[suggestion_slot])):
                                    suggested_bar_names_for_slots.add(bar_data['name'])
                            elif(suggestion_slot == 'rating'):
                                    if(Policy.check_rating(query_element,bar_data[suggestion_slot])): 
                                        suggested_bar_names_for_slots.add(bar_data['name'])
                            elif(suggestion_slot == 'hours'):
                                if(Policy.check_hours(query_element,bar_data[suggestion_slot])):
                                    suggested_bar_names_for_slots.add(bar_data['name'])
                            elif(query_element in Policy.get_slot_data(bar_data[suggestion_slot])):
                                suggested_bar_names_for_slots.add(bar_data['name'])
                    list_of_suggested_bars.append(suggested_bar_names_for_slots)

                bar_names = set.intersection(*list_of_suggested_bars)
                sys_act = SysAct()  
                sys_act.type = SysActionType.RetunSuggestion

                sys_act.add_value('names', '\n\n' + '\n'.join(list((bar_names))) + '\n\n\n')  
            except Exception as ex:
#                print(ex)
                sys_act = SysAct()
                sys_act.type = SysActionType.Bad
        else:
            sys_act, sys_state = self._next_action(beliefstate)
            
        if self.logger:
            self.logger.dialog_turn("System Action: " + str(sys_act))
        if "last_act" not in sys_state:
            sys_state["last_act"] = sys_act
        return {'sys_act': sys_act, "sys_state": sys_state}

    def get_pincode_from_address(address):
         
        pattern = r"\b\d{5}\b"   

        # Search for the pattern in the address
        match = re.search(pattern, address)

        if match:
            return match.group()
        else:
            return None
        
    def filter_by_region(query,bars_data):

        #landmarks
        east = "Nannina, Stuttgart"
        north = "Nordbahnhof, Stuttgart"
        south = "university stuttgart"
        west = "Pinsa Manufaktur Stuttgart"
        mitte = "Schlossplatz Stuttgart"

        if("near" in query):
            requested_location = query.split("near")[1]
        elif("around" in query):
            requested_location = query.split("around")[1]
        else:
            requested_location = mitte


        if("east" in requested_location):
            pincode = Policy.get_pincode(east)
            requested_location = east
        elif("west" in requested_location):
            pincode = Policy.get_pincode(west)
            requested_location = west

        elif("north" in requested_location):
            pincode = Policy.get_pincode(north)
            requested_location = north

        elif("south" in requested_location):
            pincode = Policy.get_pincode(south)
            requested_location = south

        elif("center" in requested_location or "mitte" in requested_location):
            pincode = Policy.get_pincode(mitte)
            requested_location = mitte

        elif("near" in requested_location or "me" in requested_location):
            pincode = Policy.get_pincode(south)
            requested_location = south
        else:
            pincode = Policy.get_pincode(requested_location)


        filtered_bars = set()
        filtered_bars = Policy.get_bar_for_pincodes(bars_data, [pincode], filtered_bars)
        if(len(filtered_bars) == 0):
            search_distance = 1000
            pincodes = None
            while(pincodes==None):
                pincodes = Policy.get_nearby_postcodes(requested_location,search_distance)
                search_distance = search_distance+1000
            filtered_bars = Policy.get_bar_for_pincodes(bars_data,pincodes,filtered_bars)
        return filtered_bars
 

    def get_bar_for_pincodes( bars_data, pincodes, filtered_bars):
        for bar in bars_data:
            address = bar['location']
            bar_pincode = Policy.get_pincode_from_address(address)
            for pincode in pincodes:
                if(pincode == bar_pincode):
                    filtered_bars.add(bar['name'])
        return filtered_bars

    

    def get_geocode(api_key, address):
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "key": api_key,
            "address": address,
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data["status"] == "OK" and "results" in data and len(data["results"]) > 0:
            location = data["results"][0]["geometry"]["location"]
            latitude = location["lat"]
            longitude = location["lng"]
            return latitude, longitude
        else:
            return None

    def get_nearby_places(api_key, location, radius, keyword):
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            "key": api_key,
            "query": keyword,
            "location": location,
            "radius": radius,
        }

        response = requests.get(url, params=params)
        data = response.json()
        return data.get("results", [])

    def extract_postal_codes(results):
        postal_codes = set()
        for place in results:
            postal_codes.add(place.get("formatted_address"))
        return postal_codes

    def get_nearby_postcodes(location,distance):
        # Replace 'YOUR_API_KEY' with your actual API key
        api_key = "AIzaSyCS9vPCSBAQg1WdA4uWs7u31bALNPcBbXY"
        location_name = location #"Schlossplatz Stuttgart"  # Replace with the location name (address)
        radius = distance  # Radius in meters
        keyword = "restaurant"  # Keyword to search for nearby places

        # Get latitude and longitude from the location name
        location = Policy.get_geocode(api_key, location_name)

        if location:
            # Get nearby places
            results = Policy.get_nearby_places(api_key, f"{location[0]},{location[1]}", radius, keyword)
            # Extract postal codes from the results
            addresses = Policy.extract_postal_codes(results)
            postcodes = set()
            for address in addresses:
                postcode = Policy.get_pincode_from_address(address)
                postcodes.add(postcode)

            # Print the postal codes
#            print("Nearby Postal Codes:", postcodes)
            num_elements = int(len(postcodes) * 0.7)
            sorted_set = list(postcodes)
#            print(num_elements)
            top_percent_values = set(sorted_set[:-num_elements])
#            print("Nearby Postal Codes:", top_percent_values)

            return top_percent_values
        else:
            print("Invalid location name or geocoding failed.")




    def get_pincode(location):

        try:
            api_key = "AIzaSyCS9vPCSBAQg1WdA4uWs7u31bALNPcBbXY" # private API Key - delete this later
            address_text = location
            address = address_text

            url = "https://maps.googleapis.com/maps/api/geocode/json"
            params = {
                "key": api_key,
                "address": address,
            }

            response = requests.get(url, params=params)
            data = response.json()

            if data["status"] == "OK" and "results" in data and len(data["results"]) > 0:
                for component in data["results"][0]["address_components"]:
                    if "postal_code" in component["types"]:
                        return int(component["long_name"])
            return 70182
        except:
            return 70182 # default

    # can use this for synonyms - later on maybe
    def get_synonyms(word):
        synonyms = set()
        for synset in wordnet.synsets(word):
            for lemma in synset.lemmas():
                synonyms.add(lemma.name())
        return synonyms
    def check_price_rating(user_choice,bar_price_rating_string):
        cheap_rating = '€'
        avg_rating = '€€'
        expensive_rating = '€€€'
        if("cheap" in user_choice ): # add synonyms
            if(bar_price_rating_string == cheap_rating):
                return True
        elif( "average"in user_choice ):
            if(bar_price_rating_string == avg_rating):
                return True
        elif( "expensive"in user_choice ):
            if(bar_price_rating_string == expensive_rating):
                return True
        else:
            return False
        return False    

    def check_rating(user_choice,bar_rating_string):
        user_rating = 0
        bar_rating = 0
        bad_rating = 3.3
        good_rating = 4.2
        best_rating = 4.7

        try:
            bar_rating = float(bar_rating_string)
            user_rating = float(user_choice)
        except:
            user_rating = 6
        if("good" in user_choice):
            if(bar_rating>good_rating):
                return True
        elif("best" in user_choice):
            if(bar_rating>best_rating):
                return True
        elif("bad" in user_choice):
            if(bar_rating<bad_rating):
                return True
        elif("average" in user_choice):
            if(bar_rating>bad_rating and bar_rating<good_rating):
                return True            
        elif(bar_rating>user_rating):
                return True
        else:
            return False
    
        return False





    def get_slot_data(text):
        complete_data_list = text.split('~')
        filtered_data = []
        for data in complete_data_list:
            if("No" in data):
                continue
            else:
                filtered_data.append(data.lower())
        return '~'.join(filtered_data)

    def get_postcode_from_address(api_key, address):

        api_key = "AIzaSyCS9vPCSBAQg1WdA4uWs7u31bALNPcBbXY"
        address_text = "University Stuttgart"

        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "key": api_key,
            "address": address,
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data["status"] == "OK" and "results" in data and len(data["results"]) > 0:
            for component in data["results"][0]["address_components"]:
                if "postal_code" in component["types"]:
                    return component["long_name"]
        return "70182"

    def get_distance_between_places(api_key, origin, destination):

        api_key = "AIzaSyCS9vPCSBAQg1WdA4uWs7u31bALNPcBbXY"
        origin_location = "University Stuttgart"
        destination_location = "Holzmaler Stuttgart"

        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            "key": api_key,
            "origins": origin,
            "destinations": destination,
        }

        response = requests.get(url, params=params)

        data = response.json()
        print(data)
    #    return data

        if data['status'] == 'OK' and  len(data['rows']) > 0:
            elements = data['rows'][0]['elements']
    #        print(elements)
            if "status" in elements[0] and elements[0]["status"] == "OK":
                distance_text = elements[0]["distance"]["text"]
                return distance_text
            else:
                return None
        else:
            return None

    def get_stop_words():
        stop_words = set(stopwords.words('english'))
        stop_words.add('bar')
        stop_words.add('bars')
        stop_words.add('suggest')
        stop_words.add('take')
        stop_words.add('takes')
        stop_words.add('accept')
        stop_words.add('accepts')
        stop_words.add('')
        stop_words.add(' ')

        return stop_words

    def tokenize_sentence(text):

        # Tokenize the text into words
        words = word_tokenize(text)

        # Filter out stopwords
        stop_words = Policy.get_stop_words()

        filtered_words = [word for word in words if word.lower() not in stop_words]
        filtered_words = words
        # Create a bigram finder from the filtered words
        bigram_finder = BigramCollocationFinder.from_words(filtered_words)

        # Get the top 5 bigrams (multi-word phrases) by frequency
        top_bigrams = bigram_finder.nbest(nltk.collocations.BigramAssocMeasures().raw_freq, 5)

        # Convert the bigrams to strings
        multi_word_phrases = [" ".join(bigram) for bigram in top_bigrams]


        bigrams_present = [word for word in multi_word_phrases if word in text]

        filtered_bigrams = []
        for words in bigrams_present:
            contains_stop_word = False
            for word in words.split(" "):
                if(word in stop_words):
                    contains_stop_word = True
            if not (contains_stop_word):
                filtered_bigrams.append(words)


        for bigram in filtered_bigrams:
            text = text.replace(bigram,"")
        
        suggestion_query = set(text.split(" ") + filtered_bigrams) - stop_words
#        print(suggestion_query)
        return suggestion_query

    def get_bar_timings(day,hours):
        bar_opening_time = dateparser.parse(f'{day} at {hours[0]}')
        bar_closing_time = dateparser.parse(f'{day} at {hours[1]}')
        bar_closing_time = Policy.adjust_for_midnight(day,bar_closing_time)
        return bar_opening_time,bar_closing_time
    
    def adjust_for_midnight(day,time):
        threshold = 6
        threshold_time = dateparser.parse(f'{day} at {threshold}am')
        if(time< threshold_time):
            time = time + timedelta(days=1)
        return time 


    def check_hours(user_hours,bar_hours):
        try:
            user_input = user_hours.lower()
            user_input_converted = dateparser.parse(user_input)
            user_day = user_input_converted.strftime("%A")
            user_time = user_input_converted.strftime("%H:%M:%S")

            bar_hours = eval(bar_hours)

            bar_hours_for_user_day = bar_hours[user_day].split('-')
            if(bar_hours_for_user_day[0].lower() == 'closed'):
                return False
            else:        
                user_requested_time = dateparser.parse(f'{user_day} at {user_time}')
                user_requested_time = Policy.adjust_for_midnight(user_day,user_requested_time)
                bar_opening_time,bar_closing_time = Policy.get_bar_timings(user_day,bar_hours_for_user_day)
                if(user_requested_time<bar_closing_time and user_requested_time>= bar_opening_time):
                    return True
                else:
                    return False
        except Exception as ex:
            return False




    def check_reservation_availability(user_input, opening_hours):
        sys_act = SysAct()
        # Convert user input to lowercase for case-insensitive matching

        if(Policy.check_hours(user_input,opening_hours[0]['hours'])):
            sys_act.type = SysActionType.ConfirmRequest
        else:
            sys_act.type = SysActionType.DeclineRequest
        return sys_act
  

    
    def _next_action(self, beliefstate: BeliefState):
        """Determines the next system action based on the current belief state and
           previous action.

           When implementing a new type of policy, this method MUST be rewritten

        Args:
            beliefstate (BeliefState): BeliefState object; contains all user constraints to date
            of each possible state

        Return:
            (SysAct): the next system action

        --LV
        """
        sys_state = {}
        # Assuming this happens only because domain is not actually active --LV
        if(beliefstate['makereservation']):
            try:

                
                sys_act = SysAct()
                opening_hours = self._query_db(beliefstate)
                 
                 
                user_input = beliefstate['reservation_query']
                

                sys_act = Policy.check_reservation_availability(user_input, opening_hours)

                sys_act.add_value('hours', user_input)
                name = self._get_name(beliefstate)
                sys_act.add_value(self.domain_key, name)

                sys_state['last_act'] = sys_act
                return (sys_act, sys_state)
            except:
                sys_act = SysAct()
                sys_act.type = SysActionType.Bad
                return sys_act

             
        elif UserActionType.Bad in beliefstate['user_acts'] or beliefstate['requests'] \
                and not self._get_name(beliefstate):
            sys_act = SysAct()
            sys_act.type = SysActionType.Bad
            return sys_act, {'last_act': sys_act}

        elif UserActionType.RequestAlternatives in beliefstate['user_acts'] \
                and not self._get_constraints(beliefstate)[0]:
            sys_act = SysAct()
            sys_act.type = SysActionType.Bad
            return sys_act, {'last_act': sys_act}

        elif self.domain.get_primary_key() in beliefstate['informs'] \
                and not beliefstate['requests']:
            sys_act = SysAct()
            sys_act.type = SysActionType.InformByName
            sys_act.add_value(self.domain.get_primary_key(), self._get_name(beliefstate))
            return sys_act, {'last_act': sys_act}
         
         
        results = self._query_db(beliefstate)
        sys_act = self._raw_action(results, beliefstate)

        # requests are fairly easy, if it's a request, return it directly
        if sys_act.type == SysActionType.Request:
            if len(list(sys_act.slot_values.keys())) > 0:
                sys_state['lastRequestSlot'] = list(sys_act.slot_values.keys())[0]

        # otherwise we need to convert a raw inform into a one with proper slots and values
        elif sys_act.type == SysActionType.InformByName:
            self._convert_inform(results, sys_act, beliefstate)
            # update belief state to reflect the offer we just made
            values = sys_act.get_values(self.domain.get_primary_key())
            if values:
                # belief_state['system']['lastInformedPrimKeyVal'] = values[0]
                sys_state['lastInformedPrimKeyVal'] = values[0]
            else:
                sys_act.add_value(self.domain.get_primary_key(), 'none')

        sys_state['last_act'] = sys_act
        return (sys_act, sys_state)

        
        

