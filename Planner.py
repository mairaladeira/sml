import random
import os
from OIlogic import Term, Atom, AtomSet
from Learning import Model, Rule, Effect


class Planner:
    CMD_ASP = "./clingo 1 --verbose=0 --Wno-atom-undefined "
    MOTEUR = "./moteurPlan.lp"

    HORIZON = 3

    @staticmethod
    def stateToASP(atomSet, f):
        for t in atomSet.getArgSet():
            if not t.isVar():
                f.write("object("+str(t)+").\n")
        for atom in atomSet.set:
            f.write("h("+str(atom)+",0).\n")

    @staticmethod
    def goalToASP(atomSet, horizon, f):
        for atom in atomSet.set:
            f.write(":- not h("+str(atom)+","+str(horizon)+").\n")

    @staticmethod
    def getRuleVarSet(rule):
        return rule.p.getVarSet() | rule.a.getVarSet() | rule.e.Add.getVarSet() | rule.e.Del.getVarSet()

    @staticmethod
    def getRuleArgSet(rule):
        return rule.p.getArgSet() | rule.a.getArgSet() | rule.e.Add.getArgSet() | rule.e.Del.getArgSet()

    @staticmethod
    def ruleToASP(rule,i,f):
        #get variables sets
        allTermsSet = Planner.getRuleArgSet(rule)
        allVarsSet = Planner.getRuleVarSet(rule)
        linkVars = allVarsSet - rule.a.getVarSet()
        #determine rule id and action with link variables
        rId = ""
        for var in linkVars:
            rId += str(var)+","
        if len(rId) > 0:
            rId = str(i)+",r"+"("+rId[:-1]+")"
        else:
            rId = str(i)+",r"
        act = str(rule.a)
        #define the assoc predicate, taking OI constraints into account
        body = ""
        for var in allVarsSet:
            allTermsSet.remove(var)
            body += "object("+str(var)+"), "
            for t in allTermsSet:
                body += str(var)+"!="+str(t)+", "
        if len(body) > 2:
            body = ":-" + body[:-2]
        assoc = "assoc("+act+","+rId+")"
        f.write(assoc+body+".\n")
        #preconditions
        for atom in rule.p.set:
            f.write("pre("+str(atom)+","+act+","+rId+"):- "+assoc+".\n")
        #effects
        for atom in rule.e.Add.set:
            f.write("add("+str(atom)+","+act+","+rId+"):- "+assoc+".\n")
        for atom in rule.e.Del.set :
            f.write("del("+str(atom)+","+act+","+rId+"):- "+assoc+".\n")
        #return rId for use in determining priorities
        return rId, assoc

    @staticmethod
    def modelToASP(model, f):
        for i, r in enumerate(model.rules):
            rId, ass = Planner.ruleToASP(r, i, f)

    @staticmethod
    def predictionASP(model,state,action,filename):
        with open(filename, "w") as f:
            f.write("time(0..1).\n")
            f.write("occ("+str(action)+",0).\n")
            f.write("%initial state\n")
            Planner.stateToASP(state, f)
            f.write("%Rules\n")
            Planner.modelToASP(model,f)
            with open(Planner.MOTEUR, "r") as fmoteur:
                for l in fmoteur.readlines():
                    f.write(l)
            f.write("%printing prediction\n")
            f.write("ans(F) :- h(F,1).\n")
            f.write("#show ans/1.\n")

    @staticmethod
    def predict(model, state, action):
        Planner.predictionASP(model, state, action, "tmp_Pred.lp")
        cmd = Planner.CMD_ASP+" tmp_Pred.lp > out.tmp"
        os.system(cmd)
        res = []
        with open("out.tmp", "r") as f:
            answerSet = f.readline()
            if answerSet.startswith("UNSAT"):
                #print "No effect"
                return state
            for ans in answerSet.split():
                atomStr = ans[4:-1]
                atom = Atom.parse(atomStr)
                res.append(atom)
        return AtomSet(res)


    @staticmethod
    def planASP(model, state, goal, actions, horizon, filename):
        with open(filename, "w") as f:
            f.write("time(0.."+str(horizon)+").\n")
            for act in actions:
                f.write("action("+str(act)+").\n")
            f.write("1{occ(A,T):action(A)}1:-time(T),T<"+str(horizon)+".\n")
            f.write("%initial state\n")
            Planner.stateToASP(state, f)
            f.write("%goal\n")
            Planner.goalToASP(goal, horizon, f)
            f.write("%Rules\n")
            Planner.modelToASP(model, f)
            with open(Planner.MOTEUR, "r") as fmoteur:
                for l in fmoteur.readlines():
                    f.write(l)
            f.write("%printing first action of first plan\n")
            f.write("ans(A) :- occ(A,0).\n")
            f.write("#show ans/1.\n")

    @staticmethod
    def plan(model, state, goal, actions):
        n = Planner.HORIZON
        i = 1
        while i <= n:
            Planner.planASP(model, state, goal, actions, i, "tmp_Plan.lp")
            cmd = Planner.CMD_ASP+" tmp_Plan.lp > out.tmp"
            os.system(cmd)
            with open("out.tmp", "r") as f:
                answerSet = f.readline()
                if not answerSet.startswith("UNSAT"):
                    #print "Plan :",answerSet[4:-2]
                    return Atom.parse(answerSet[4:-2])
            i += 1
        return None
