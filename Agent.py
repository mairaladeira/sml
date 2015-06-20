__author__ = 'Maira'

from Environment import Env
from OIlogic import Subst
from Learning import Effect
from Planner import Planner
import sys


class Agent:
    def __init__(self, env, sizeEp, npMaxSteps):
        # Env containing the environment in which the agent is evolving
        self.env = env
        # int giving the size of an episode (max number of action the agent
        # given to reach his goal)
        self.sizeEp = sizeEp
        # total number of actions before stopping
        self.maxStep = npMaxSteps
        # Model containing the current action theory of the agent
        self.theory = self.env.get_model()
        # current state
        self.state = self.env.generateState()
        # current goal
        self.goal = self.env.generateGoal(self.state)

    def __str__(self):
        s = 'Agent:{\n'
        s += '    '+str(self.theory)
        s += '    Current State: '+str(self.state)+'\n'
        s += '    Current Goal: '+str(self.goal)+'\n'
        s += '    Episode size: '+str(self.sizeEp)+'\n'
        s += '    Max Step: '+str(self.maxStep)+'\n'
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
    if len(sys.argv) == 1:
        print('Please specify the size of the episode and the number total of steps.')
        print('Usage: python Agent.py -es <episode_size> -ts <total_steps>')
        exit()
    else:
        """
        1. Decide which action to take
        2. Perform the action and observe the result
        3. Learn from this experience
        4. Check if goal or time_limit:
            - register success or failure
        """
        args = sys.argv
        if len(args) != 5 or args[1] != '-es' or args[3] != '-ts':
            print('Usage: python Agent.py -es <episode_size> -ts <total_steps>')
            exit()
        # It is advised to test and debug with 4 blocks, but i don't understand why
        env = Env(4)
        agent = Agent(env, int(args[2]), int(args[4]))
        model = env.get_model()
        state = env.generateState()
        actions = env.getAllActions()
        goal = env.generateGoal(state)
        plan = Planner.plan(model, state, goal, actions)
        print(agent)
        #print('Add initialization of agent here')