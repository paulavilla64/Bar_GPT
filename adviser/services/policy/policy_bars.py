from services.service import PublishSubscribe
from utils import SysAct, SysActionType
from adviser.utils.beliefstate import BeliefState
from adviser.services.policy.policy_handcrafted import HandcraftedPolicy
from utils.useract import UserActionType

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
        # handle domain specific actions
        else:
            sys_act, sys_state = self._next_action(beliefstate)
        if self.logger:
            self.logger.dialog_turn("System Action: " + str(sys_act))
        if "last_act" not in sys_state:
            sys_state["last_act"] = sys_act
        return {'sys_act': sys_act, "sys_state": sys_state}

        
        

