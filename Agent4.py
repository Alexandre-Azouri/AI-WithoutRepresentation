from resources import Interaction


class Agent4:
    def __init__(self, valence_table):
        """ Creating our agent """
        self.lastInteraction = None
        self.valence_table = valence_table
        self._action = None
        self.anticipated_outcome = None
        self.lastAction = None
        self.obtainedOutcomes = {}
        self.counter = 0

    def action(self, outcome):
        """ tracing the previous cycle """
        if self._action is not None:
            print("Action: " + str(self._action) +
                  ", Anticipation: " + str(self.anticipated_outcome) +
                  ", Outcome: " + str(outcome) +
                  ", Satisfaction: (anticipation: " + str(self.anticipated_outcome == outcome) +
                  ", valence: " + str(self.valence_table[self._action][outcome]) + ")")
            self.lastInteraction.outcome = outcome
            self.lastInteraction.valence = self.valence_table[self._action][outcome]

        """ Computing the next action to enact """
        # TODO: Implement the agent's decision mechanism - DONE
        self.counter += 1
        value = None
        if self.lastAction is not None:
            value = self.valence_table[self.lastAction][outcome]
        elif self._action is None:
            self._action = 0

        if value is not None and value < 0:
            self._action = self.chosePosAction()
        if self.counter > 3:
            self._action = (self._action + 1) % len(self.valence_table)
            self.counter = 0

        # TODO: Implement the agent's anticipation mechanism - DONE
        self.anticipated_outcome = None
        newest_interactions = Interaction(self._action, None, None)
        if (self.obtainedOutcomes.get(
                self.lastInteraction.__hash__())
                is None and self.lastAction is not None):
            self.obtainedOutcomes[self.lastInteraction.__hash__()] = {self._action: newest_interactions}
        elif (self.obtainedOutcomes.get(self.lastInteraction.__hash__()) is not None
              and self._action not in self.obtainedOutcomes[self.lastInteraction.__hash__()]):
            self.obtainedOutcomes[self.lastInteraction.__hash__()][self._action] = newest_interactions
        elif (self.obtainedOutcomes.get(self.lastInteraction.__hash__()) is not None
              and self._action in self.obtainedOutcomes[self.lastInteraction.__hash__()]):
            self.anticipated_outcome = self.obtainedOutcomes[self.lastInteraction.__hash__()][self._action].outcome

        if self.lastAction != self._action:
            self.counter = 0
        self.lastAction = self._action
        self.lastInteraction = newest_interactions
        return self._action

    def chosePosAction(self):
        valence = [0, 0, 0]
        iterations = self.obtainedOutcomes.get(self.lastInteraction.__hash__())
        for i in range(0, len(self.valence_table)):
            if iterations is not None and i in iterations:
                valence[i] = iterations[i].valence
        value = valence.index(max(valence))
        if (value == self.lastAction):
            valence.pop(value)
        return valence.index(max(valence))
