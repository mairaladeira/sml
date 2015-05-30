import random
import os
from OIlogic import Term, Atom, AtomSet
from Learning import Model, Rule, Effect
from Planner import Planner


class Env:
    @staticmethod
    def model7B2C():
        res = Model()
        A = Term("A")
        B = Term("B")
        C = Term("C")
        X = Term("X")
        Y = Term("Y")
        floor = Term("floor")
        clA = Atom("clear\\1", [A])
        clB = Atom("clear\\1", [B])
        clC = Atom("clear\\1", [C])
        onAB = Atom("on\\2", [A, B])
        onAf = Atom("on\\2", [A, floor])
        onAC = Atom("on\\2", [A, C])
        colAX = Atom("color\\2", [A, X])
        colAY = Atom("color\\2", [A, Y])
        colBX = Atom("color\\2", [B, X])
        colBY = Atom("color\\2", [B, Y])
        movAB = Atom("move\\2", [A, B])
        movAf = Atom("move\\2", [A, floor])
        r1 = Rule(AtomSet([clA, onAB]), movAf, Effect(AtomSet([onAf, clB]), AtomSet([onAB])))
        r2 = Rule(AtomSet([clA, clB, colAX, colBX, onAf]), movAB, Effect(AtomSet([onAB]), AtomSet([clB, onAf])))
        r3 = Rule(AtomSet([clA, clB, colAX, colBX, onAC]), movAB, Effect(AtomSet([onAB, clC]), AtomSet([clB, onAC])))
        r4 = Rule(AtomSet([clA, clB, colAX, colBY]), movAB, Effect(AtomSet([colAY]), AtomSet([colAX])))
        res.addRule(r1)
        res.addRule(r2)
        res.addRule(r3)
        res.addRule(r4)
        return res

    def __init__(self, nbBlocks):
        self.model = Env.model7B2C()
        self.nbBl = nbBlocks

    def get_model(self):
        return self.model

    def do(self, state, action):
        return Planner.predict(self.model,state,action)

    def generateState(self):
        a = Term("a")
        b = Term("b")
        c = Term("c")
        d = Term("d")
        e = Term("e")
        f = Term("f")
        g = Term("g")
        blank = Term("blank")
        floor = Term("floor")
        wht = Term("white")
        blk = Term("black")
        Colors = [wht, blk]
        L = [a, b, c, d, e, f, g]
        L = L[:self.nbBl]
        for i in xrange(21-self.nbBl):
            L.append(blank)
        random.shuffle(L)
        T = [L[0:7], L[7:14], L[14:]]
        L_state = []
        for tower in T:
            Lt = [t for t in tower if t != blank]
            b2 = floor
            for (i, block) in enumerate(Lt):
                L_state.append(Atom("on\\2", [block, b2]))
                L_state.append(Atom("color\\2", [block, random.choice(Colors)]))
                b2 = block
            if b2 != floor:
                L_state.append(Atom("clear\\1",[b2]))
        return AtomSet(L_state)

    def generateGoal(self, state):
        actions = self.getAllActions()
        st1 = state
        acts = []
        while len(acts) < 4:
            act = random.choice(actions)
            newS = self.do(st1,act)
            if newS != st1:
                acts.append(act)
                st1 = newS
        #rint "GoalState : ",st1
        goal = list(set(st1.set)-set(state.set))
        #k = random.randint(3, len(st1.set) - 1)
        k = random.randint(3, len(state) - 1)
        for i in xrange(k):
            #sup = random.choice(st1.set)
            sup = random.choice(state.set)
            if sup not in goal:
                goal.append(sup)
        return AtomSet(goal)

    def getAllActions(self):
        a = Term("a")
        b = Term("b")
        c = Term("c")
        d = Term("d")
        e = Term("e")
        f = Term("f")
        g = Term("g")
        floor = Term("floor")
        LX = [a, b, c, d, e, f, g]
        LX = LX[:self.nbBl]
        LY = [floor]+LX
        res = []
        for x in LX:
            for y in LY:
                if x != y:
                    res.append(Atom("move\\2", [x, y]))
        return res