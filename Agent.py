__author__ = 'Maira'

from Environment import Env
from OIlogic import Subst

class Agent:
    def __init__(self, env, sizeEp, npMaxSteps):
        self.env = env
        self.sizeEp = sizeEp
        self.maxStep = npMaxSteps
        self.theory = None
        self.state = None
        self.goal = None

    def __str__(self):
        s = '{'
        s += '('+str(self.theory)+'),'
        s += '('+str(self.env)+'),'
        s += '('+str(self.state)+'),'
        s += '('+str(self.goal)+'),'
        s += '('+str(self.sizeEp)+'),'
        s += '('+str(self.maxStep)+')'
        s += '}'
        return s

    """
    Returns an Atom representing the action that the agent with undertake.
    Either the first action or randomly choose from a list of actions.
    """
    def decide(self):
        return

    """
    Run the Agent code
    """
    def run(self):
        return

if __name__ == "__main__":
    env = Env(4)
    rules = env.get_model().get_rules()
    state = env.generateState()
    actions = env.getAllActions()
    effect = env.generateGoal(state)
    #print(effect)
    for a in actions:
        for r in rules:
            if r.wellformed():
                ra = r.a
                s1 = Subst([], [])
                pre_m = r.prematch(state, a, s1)
                post_m = r.postmatch(a, effect, s1)

    print('Add initialization of agent here')