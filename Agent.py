__author__ = 'Maira'

from Environment import Env
from OIlogic import Subst
from Learning import Effect, Example
from Planner import Planner
import sys
import random


class Agent:
    def __init__(self, env, sizeEp, npMaxSteps):
        self.env = env
        self.sizeEp = sizeEp
        self.maxStep = npMaxSteps
        self.theory = self.env.get_model()
        self.state = None
        self.goal = None

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
        actions = self.env.getAllActions()
        u_act = Planner.plan(self.theory, self.state, self.goal, actions)
        #print(u_act)
        if u_act is None:
            u_act = random.choice(actions)
        return u_act

    """
    Run the Agent code
    """
    def run(self):
        print(self.env.get_model())
        for j in range(0, self.sizeEp):
            self.state = self.env.generateState()
            self.goal = self.env.generateGoal(self.state)
            print('Goal: '+str(self.goal))
            success = False
            for i in range(0, self.maxStep):
                action_undertake = self.decide()
                new_state = self.env.do(self.state, action_undertake)
                example = Example(self.state, action_undertake, Effect.getEffect(self.state, new_state))
                self.env.get_model().IRALe(example)
                self.state = new_state
                if self.goal.toSet().issubset(self.state.toSet()):
                    print('SUCCESS')
                    success = True
                    break
            if not success:
                print('FAIL')

        print(self.env.get_model())

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
        agent.run()
