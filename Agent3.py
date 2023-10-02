
class Agent3:
    def __init__(self, valence_table):
        """ Creating our agent """
        self.valence_table = valence_table
        self._action = None
        self.anticipated_outcome = None
        self.counter = 0
        self.lastAction = None
        self.obtainedOutcomes = {}

    def action(self, outcome):
        """ tracing the previous cycle """
        if self._action is not None:
            print("Action: " + str(self._action) +
                  ", Anticipation: " + str(self.anticipated_outcome) +
                  ", Outcome: " + str(outcome) +
                  ", Satisfaction: (anticipation: " + str(self.anticipated_outcome == outcome) +
                  ", valence: " + str(self.valence_table[self._action][outcome]) + ")")

        """ Computing the next action to enact """
        # TODO: Implement the agent's decision mechanism
        self.counter += 1
        value = None
        if(self.lastAction is not None):
            value = self.valence_table[self.lastAction][outcome]
        if(self._action is None):
            self._action = 0

        if(value is not None and value < 0):
            self._action = self.chosePosAction() if self.chosePosAction() is not None else self.lastAction
        if(self.counter > 3):
            self._action = (self._action +1) %3
            self.counter = 0
        # TODO: Implement the agent's anticipation mechanism
        self.anticipated_outcome = 0
        if(self.obtainedOutcomes.get(self.lastAction) is None and self.lastAction is not None):
            self.obtainedOutcomes[self.lastAction] = outcome

        if(self.obtainedOutcomes.get(self._action) is not None):
            self.anticipated_outcome = self.obtainedOutcomes[self._action]
        if(self._action != self.lastAction):
            self.counter = 0
        self.lastAction = self._action
        return self._action

    def chosePosAction(self):
        for key in self.obtainedOutcomes.keys():
            value = self.valence_table[key][self.obtainedOutcomes[key]]
            if(value > 0):
                if(key != self.lastAction):
                    return key
        return None