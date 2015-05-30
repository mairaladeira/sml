__author__ = 'Maira'

from Environment import Env

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
    print('Add initialization of agent here')