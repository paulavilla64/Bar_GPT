from services.service import PublishSubscribe
from utils import SysAct, SysActionType
from utils.beliefstate import BeliefState
from services.policy.policy_handcrafted import HandcraftedPolicy
from utils.useract import UserActionType
import json


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

        # removes hello and thanks if there are also domain specific actions
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
            suggestion_slots = set(beliefstate['suggestion_slot'].split("~"))
            suggestion_slots.discard("")
            suggestion_slots.discard(" ")
            suggestion_query = set(beliefstate['reservation_query'].split(" "))
#            suggestion_slot = 'offerings'
#            suggestion_query = 'beer'
            beliefstate['informs'] = {}
            db_data = self._query_db(beliefstate)
            # filter data
            bar_names = []
            print(db_data)
            for dic in db_data:
                for suggestion_slot in suggestion_slots:
                    for query in suggestion_query:
                        if(query in dic[suggestion_slot]):
                            bar_names.append(dic['name'])

            sys_act = SysAct() # make some change here to get data from db ... filter data and return new system act with list of bars
            sys_act.type = SysActionType.RetunSuggestion

            sys_act.add_value('names', '\n\n' + '\n'.join(list(set(bar_names))) + '\n\n\n')  
        else:
            sys_act, sys_state = self._next_action(beliefstate)
            
        if self.logger:
            self.logger.dialog_turn("System Action: " + str(sys_act))
        if "last_act" not in sys_state:
            sys_state["last_act"] = sys_act
        return {'sys_act': sys_act, "sys_state": sys_state}
    
    # check if the time is given in am or pm
    def check_am_and_pm(time):
        int_time = 0
        if "am" in time:
            int_time = int(time.replace("am", "").strip())
            if int_time < 12 and int_time >=6:
                int_time = int_time
            else:
                int_time = int_time + 24
        elif "pm" in time:
            int_time = int(time.replace("pm", "").strip()) + 12
        return int_time

    
    def check_reservation_availability(user_input, opening_hours):
        sys_act = SysAct()
        # Convert user input to lowercase for case-insensitive matching
        user_input = user_input.lower()

        # Extract the requested day and time from the user input
        requested_day, requested_time = user_input.split()
        print(requested_day, requested_time)

        # Extracting the dictionary from the list
        try:
            hours_dict = json.loads(opening_hours[0]['hours'])
            # Converting keys to lowercase
            hours_dict = {key.lower(): value for key, value in hours_dict.items()}
        except:
            sys_act.type = SysActionType.DeclineRequest
            return sys_act

        if requested_day in hours_dict:
            if hours_dict[requested_day] == 'Closed':
                sys_act.type = SysActionType.DeclineRequest
                return sys_act
            
        # Converting keys to lowercase
        hours_dict = {key.lower(): value for key, value in hours_dict.items()}
        hours_index = hours_dict[requested_day].split(" - ")
        print(hours_index)
        starting_hours = Policy.check_am_and_pm(hours_index[0])
        print(starting_hours)
        closing_hours = Policy.check_am_and_pm(hours_index[1])
        user_time = Policy.check_am_and_pm(requested_time)
        print(user_time)
        print(f"{starting_hours} {closing_hours} {user_time}")
        # Check if the requested day and time match the opening hours
        if requested_day in hours_dict:
            if hours_dict[requested_day] == "Closed":
                sys_act.type = SysActionType.DeclineRequest
                

            elif user_time >= starting_hours and user_time <= closing_hours:
                
                sys_act.type = SysActionType.ConfirmRequest

            else:
                sys_act.type = SysActionType.DeclineRequest

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

            # opening times from database
            sys_act = SysAct()
            opening_hours = self._query_db(beliefstate)
            # print(f"This are the opening hours {opening_hours}")
            # print(type(opening_hours))

            #user_input
            user_input = beliefstate['reservation_query']
            # print(f"This is the user input {user_input}")
            # print(type(user_input))

            sys_act = Policy.check_reservation_availability(user_input, opening_hours)

            sys_act.add_value('hours', user_input)
            name = self._get_name(beliefstate)
            sys_act.add_value(self.domain_key, name)

            sys_state['last_act'] = sys_act
            return (sys_act, sys_state)

            # get hours from database
            # call function  which checks if booking possibel
            # if booking possible create sys_act which says booking done
            # else create sys act which says booking not possible 
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
        # Check if UserActionType.Booking(perform booking) in belifstate request
        # if yes
            # create system act with Booking or booking mode or sometyhign
            # systemact . add value check timings ( maybe set inform to get timings) and confirm booking

            # Handle the "make a reservation" user act
        
        
        # Otherwise we need to query the db to determine next action
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

        
        

