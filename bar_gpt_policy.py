from adviser.utils.beliefstate import BeliefState
from adviser.services.policy.policy_handcrafted import HandcraftedPolicy

class Policy(HandcraftedPolicy):
    def __init__(self, domain, logger, max_turns):
        super().__init__(domain, logger, max_turns)
        policy = HandcraftedPolicy()
        """
        Initializes the policy
        """

    def choose_sys_act(self, beliefstate: BeliefState) -> dict:
        """
        Responsible for walking the policy through a single turn. Uses the current user
        action and system belief state to determine what the next system action should be.

        To implement an alternate policy, this method may need to be overwritten

        Args:
            belief_state (BeliefState): a BeliefState obejct representing current system knowledge

        Returns:
            (dict): a dictionary with the key "sys_act" and the value that of the systems next action
        """
        
        # Add additional rules/functionality
        # Add "Make a reservation" as System act?
        return super().choose_sys_act(beliefstate)

