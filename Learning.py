__author__ = 'Maira'


class Model:
    def __init__(self):
        self.rule = []
        self.ex = []

    def addRule(self, rule):
        self.rule = rule

    def memorizeEx(self, ex):
        self.ex = ex

    def specialize(self, rule):
        return

    def getUncovEx(self, rule):
        return

    def contradicted(self, rule):
        return True

    def generalize(self, examples):
        return

    def IRALe(self, ex):
        return

class Rule:
    def __init__(self, state, action, effect):
        self.state = state
        self.action = action
        self.effect = effect
        self.anc = None

    def wellformed(self):
        return True

    def prematch(self, gstate, gaction, sigma):
        return

    def postmatch(self, gstate, geffect, sigma):
        return

    def covers(self, ex):
        return

    def postgeneralize(self, ex, ownSubst, exSubst):
        return


class Effect:
    def __init__(self, pos, neg):
        self.Add = pos
        self.Del = neg

    def getEffect(self, prevState, newState):
        return

    def filterOI(self, other, subst):
        atoms = []
        return atoms