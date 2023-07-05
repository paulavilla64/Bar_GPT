from services.service import PublishSubscribe
from utils import SysAct, SysActionType
from utils.beliefstate import BeliefState
from services.policy.policy_handcrafted import HandcraftedPolicy
from utils.useract import UserActionType

# Define the utility function to extract day, start_time, and end_time from hours_string
def extract_hours_slot(hours_string):
    day, time_range = hours_string.split('\t ')
    start_time, end_time = time_range.split(' - ')
    return day, start_time, end_time

def check_reservation_availability(day, start_time, end_time):
    # Check if the bar is open on the specified day and during the specified time
    # Your implementation here
    return True  # Replace this with your actual logic to determine reservation availability


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

        else:
            sys_act, sys_state = self._next_action(beliefstate)
        
            # handle make a reservation user act
        if UserActionType.MakeReservation in beliefstate["user_acts"]:
            sys_act = SysAct()
            sys_act.type = SysActionType.MakeReservation

            # check if a reservation is possible on that day and time
            # hours_slot_value = beliefstate["informs"]["hours"] 
            # day, start_time, end_time = extract_hours_slot(hours_slot_value)
            # reservation_is_possible = check_reservation_availability(day, start_time, end_time)

            # if reservation_is_possible:
            #     sys_act = SysAct()
            #     sys_act.type = SysActionType.ConfirmReservation
            # else:
            #     sys_act = SysAct()
            #     sys_act.type = SysActionType.ReservationNotPossible

        if self.logger:
            self.logger.dialog_turn("System Action: " + str(sys_act))
        if "last_act" not in sys_state:
            sys_state["last_act"] = sys_act
        return {'sys_act': sys_act, "sys_state": sys_state}
    
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
        if UserActionType.Bad in beliefstate['user_acts'] or beliefstate['requests'] \
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

            # Handle the "make a reservation" user act
        elif UserActionType.MakeReservation in beliefstate['user_acts']:
            beliefstate["sys_acts"].append(SysActionType.MakeReservation)
            sys_act = SysAct()
            sys_act.type = SysActionType.MakeReservation
            # Add any necessary slots or values for the reservation
            sys_act.add_value("makereservation")
            #sys_act.add_value("party_size")
            return sys_act, {'last_act': sys_act}
        
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

        
        

