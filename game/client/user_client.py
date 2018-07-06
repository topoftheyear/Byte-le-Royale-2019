from game.common.enums import  *

class UserClient:

    def __init__(self):
        self.reset_actions()


    def reset_actions(self):

        self._action = PlayerAction.none
        self._action_param_1 = None
        self._action_param_2 = None
        self._action_param_3 = None

        self._move_action = None

    def team_name(self):
        return "ForgotToSetAName"

    def move(self, x, y):

        self._move_action = (x, y)


