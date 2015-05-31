__author__ = 'Maira'

from OIlogic import Atom, AtomSet, Subst
import copy

class Effect:
    def __init__(self, pos, neg):
        self.Add = pos
        self.Del = neg

    def __str__(self):
        s = '{'
        s += 'Add: '+str(self.Add)+', '
        s += 'Del: '+str(self.Del)
        s += '}'
        return s

    #def add_atom(self, atom):
        #self.Add.append(atom)

    #def del_atom(self, atom):
        #if atom in self.Del:
            #self.Del.remove(atom)

    def __eq__(self, other):
        return self.Add.toSet().__eq__(other.Add.toSet()) and self.Del.toSet().__eq__(other.Del.toSet())

    def apply(self, subst):
        return Effect(self.Add.apply(subst), self.Del.apply(subst))

    """
    Gets previous and new state and return the effect.
    Use the method toSet from AtomSet class in order to get the
    content of each state as a set of atoms
    """
    @staticmethod
    def getEffect(prevState, newState):
        prev_atoms = prevState.toSet()
        new_atoms = newState.toSet()
        # finds difference in sets
        add_atoms = list(new_atoms.difference(prev_atoms))
        del_atoms = list(prev_atoms.difference(new_atoms))

        return Effect(AtomSet(add_atoms), AtomSet(del_atoms))

    """
    Return the list of atoms of all OI extensions theta of OI substitution subst,
    such that theta.Add = other.Add and theta.Del = other.Del
    """
    def filterOI(self, other, s=Subst([],[])):
        # Union of sets
        self_union = self.Add.toSet() | self.Del.toSet()
        other_union = other.Add.toSet() | other.Del.toSet()
        # Atomsets
        self_atom_set = AtomSet(list(self_union))
        other_atom_set = AtomSet(list(other_union))
        return self_atom_set.filterIncOI(other_atom_set, s)

    #maybe new functions have to be added.


class Example:
    def __init__(self, state, action, effect):
        self.s = state
        self.a = action
        self.e = effect
        self.name = ''

    def __str__(self):
        s = '{'
        s += 'State: '+str(self.s)+', '
        s += 'Action: '+str(self.a)+', '
        s += 'Effect: '+str(self.e)
        s += '}'
        return s

    def set_name(self, name):
        self.name = name


class Rule(Example):
    def __init__(self, state, action, effect):
        Example.__init__(self, state, action, effect)
        self.anc = None

    def __eq__(self, other):
        return self.s == other.s and self.a == other.a and self.e == other.e \
               and self.name == other.name and self.anc == other.anc

    def set_state(self, state):
        self.s = state

    def set_name(self, name):
        self.name = name

    def set_anc(self, ans_r):
        self.anc = ans_r

    @staticmethod
    def compareSubst(subst_1, subst_2):
        res = True
        if len(subst_1.vars) != len(subst_2.vars) or len(subst_1.vals) != len(subst_2.vals) or \
                        len(subst_1.forbidVal) != len(subst_2.forbidVal):
            return False
        else:
            if set(subst_1.forbidVal) != set(subst_2.forbidVal):
                return False
            else:
                for elem in subst_1.vars:
                    if elem in subst_2.vars and subst_2.vals[subst_2.vars.index(elem)] == subst_1.vals[subst_1.vars.index(elem)]:
                        res *= True
                    else:
                        res *= False
        return res
    """
    This function should return true if the rule is well formed and false otherwise.
    For a rule to be well formed:
    - rule.effect.Del is contained by rule.state
    - rule.effect.Add intersection rule.state = empty
    - All vars of rule.action should occur in r.state and r.effect and r.effect may
      refer objects/variables not occuring in r.action
    """
    def wellformed(self):
        effect_del = self.e.Del.toSet()
        state = self.s.toSet()
        effect_add = self.e.Add.toSet()

        # rule.effect.Del is contained by rule.state
        condition_1 = effect_del.issubset(state)

        # rule.effect.Add intersection rule.state = empty
        if not effect_add.intersection(state):
            condition_2 = True
        else:
            condition_2 = False

        action_vars = self.a.getVarSet()
        effect_vars = self.e.Add.getVarSet().union(self.e.Del.getVarSet())
        state_vars = self.s.getVarSet()

        # All vars of rule.action should occur in r.state union r.effect and r.effect may
        # refer objects/variables not occuring in r.action
        #condition_3 = action_vars.issubset(effect_vars.union(state_vars))
        # {r.s - r.e.del} u {r.e.add}
        diff_variables = AtomSet(list(state.difference(effect_del).union(effect_add))).getVarSet()
        condition_3 = action_vars.issubset(diff_variables)
        
        return condition_1 and condition_2 and condition_3
    """
    Return the list of substitutions R of all OI extensions theta of OI
    substitution sigma such that the rule pre-matches (gstate, gaction) with
    substitution theta.
    - (r.a)sigma = gaction
    - (r.s)sigmaTheta is contained by gstate
    """
    def prematch(self, gstate, gaction, sigma=Subst([],[])):
        #condition 1: (r.a)sigma = gaction
        if not self.a.filterOI(gaction, sigma):
            return {}
        theta = self.s.filterIncOI(gstate, sigma)
        #condition 2: (r.s)sigmaTheta is contained by gstate
        for t in theta:
            app = self.s.apply(t)
            if not(app.toSet().issubset(gstate.toSet())):
                return {}
        return theta

    """
    Returns the list of substitutions R of all OI extensions theta of OI
    substitution sigma such that the rule post-matches (gstate, gaction) with
    substitution theta.
    - (r.a)invroSigma = gaction
    - (r.e)invroSigmaTheta = geffect
    """
    def postmatch(self, gaction, geffect, sigma=Subst([],[])):
        if not self.a.filterOI(gaction, sigma):
            return {}

        theta = self.e.filterOI(geffect, sigma)

        # if (r.e)theta != geffect then return empty
        if not (theta and self.e.apply(theta[0]).__eq__(geffect)):
            return {}

        return theta

    """
    Returns a (int, Subst) pair. If the rule coves ex, this function must return
    (1, theta) where theta is a substitution with which the rule covers ex. If ex
    contradicts the rule, this function must return (-1, theta) where theta is the
    substitution with which the rule pre-matches ex.  When both conditions do not
    occur, the function should return (0, None)
    """
    def covers(self, ex):
        # We will need the substitution sigma to check if both are the same
        sigma = Subst([], [])
        pre_match = self.prematch(ex.s, ex.a, sigma)
        if len(pre_match) == 0:
            return [0, None]
        else:
            post_match = self.postmatch(ex.a, ex.e, sigma)
            if len(post_match) == 0:
                return [-1, pre_match]
            else:
                # Comparison of unordered lists:
                if not Rule.compareSubst(pre_match[0], post_match[0]):
                    return [-1, pre_match]
                else:
                    return [1, post_match]

    """
    Returns either None or a Rule and updates ownSubst and exSubst.
    """
    def postgeneralize(self, ex, ownSubst=Subst([],[]), exSubst=Subst([],[])):
        gact = self.a.generalize(ex.a, ownSubst, exSubst)
        if gact:
            gadd = self.e.Add.generalizeEqOI(ex.e.Add, ownSubst, exSubst)
            for g in gadd:
                sig_1 = g[1]
                th_1 = g[2]
                gdel = self.e.Del.generalizeEqOI(ex.e.Del, sig_1, th_1)
                if gdel:
                    gpre = self.s.revApply(gdel[0][1])
                    ownSubst = gdel[0][1]
                    exSubst = gdel[0][2]
                    grule = Rule(gpre, gact, Effect(g[0], gdel[0][0]))
                    #grule.set_anc(self)
                    return grule

        else:
            return None

    """
    Returns the specialization of the rules such that it no longer
    prematches de example ex
    """
    def specialize(self, ex):
        if self.anc is None or not self.prematch(ex.s, ex.a):
            return self
        else:
            return self.anc.specialize(ex)


class Model:
    def __init__(self):
        self.rules = []
        self.exMem = []

    def get_rules(self):
        return self.rules

    def get_exMem(self):
        return self.exMem

    def __str__(self):
        s = 'Model:\n'
        s += '\tRules:\n'
        for r in self.rules:
            s += '\t\t'+str(r)+'\n'
        s += '\tExamples Memory:\n'
        for ex in self.exMem:
            s += '\t\t'+str(ex)+'\n'
        return s

    """
    Add a new rule to the Model
    """
    def addRule(self, rule):
        self.rules.append(rule)

    """
    Memorize a new example in the Model
    """
    def memorizeEx(self, ex):
        self.exMem.append(ex)

    """
    Function that specializes the model.
    Receives an example and a rule to specialize
    """
    def specialize(self, ex):
        ret = False
        to_remove = []
        to_add = []
        # Iterates over all rules
        for i, r in enumerate(self.rules):
            # In example contradicts one rule, specialize the rule:
            if r.covers(ex)[0] == -1:
                ret = True
                to_remove.append(i)
                to_add.append(r.specialize(ex))
        # Remove general rule and add specialized:
        for i in to_remove:
            self.rules.pop(i)
        self.rules.extend(to_add)

        return ret

    # Don't erase: in case we need to fit the parameters in the assignment:
    def specialize2(self, rule, ex):
        # Find the rule that will be specialized:
        rem_idx = -1
        for i, r in enumerate(self.rules):
            if r == rule:
                rem_idx = i
        # We remove the rule from the model and add its specialization:
        rem_rule = self.rules.pop(rem_idx)
        self.addRule(rem_rule.specialize(ex))

    """
    Function that specialize a rule.
    Use the field anc and the function prematch from Rule class
    """
    def specialize_old(self, rule):
        # You don't specialize vs the counterexamples in the model!
        # You specialize the rules in the model vs an example
        for ex in self.exMem:
            subst = Subst([], [])
            #not sure about this part. what to do with rules without anc?
            if not rule.prematch(ex.s, ex.a, subst) and rule.anc:
                rule = rule.anc
                self.specialize(rule)
        return rule

    """
    Return a boolean indicating if an example is covered by the model.
    If False, it means that the model is incomplete for this example
    """
    def covers(self, ex):
        ret = False
        for rule in self.rules:
            res = rule.covers(ex)
            if res[0] == 1:
                ret = True
        return ret

    """
    Return a boolean indicating if an example contradicts a rule in the model.
    If True, it means that the model is incoherent for this example
    """
    def contradicts(self, ex):
        ret = False
        # Observe that this method differs from contradicted because it iterates on the rules and not on the
        # memorized examples.
        for rule in self.rules:
            res = rule.covers(ex)
            if res[0] == -1:
                ret = True
        return ret

    """
    Return a list of examples from exMem that are not covered by the Model anymore
    """
    def getUncovEx(self):
        # Here we have to compare sel.rules with self.memEx
        uncovered_exs = []
        for ex in self.exMem:
            # Check if there exists a rule that covers the example:
            if not self.covers(ex):
                uncovered_exs.append(ex)
        return uncovered_exs

    def getUncovEx_old(self, rule): # You're right, there is no need for this parameter:
        # We need to compare vs all rules
        uncovered_exs = []
        for ex in self.exMem:
            covers = rule.covers(ex)
            if covers[0] != 1:
                uncovered_exs.append(ex)
        return uncovered_exs

    """
    Return a boolean indicating if the rule is contradicted by the Model.
    """
    def contradicted(self, rule):
        is_contradicted = False
        for ex in self.exMem:
            res = rule.covers(ex)
            if res[0] == -1:
                is_contradicted = True
        return is_contradicted

    def contradicted_old(self, rule):
        is_contradicted = False
        for ex in self.exMem:
            sigma = Subst([], [])
            pre_match = rule.prematch(ex.s, ex.a, sigma)
            post_match = rule.postmatch(ex.a, ex.e, sigma)
            #here i am saying the if the rule does not pre match or does not post match it
            # is also contradicting the model.
            # No, contradicts is when it prematches but not postmatches with same subst.
            # This is already done by the Rule.covers method:
            # if it returns [-1, theta] it means that it prematches but not postmatches => contradicts
            if len(pre_match) == 0 or len(post_match) == 0 or not Rule.compareSubst(pre_match[0], post_match[0]):
                is_contradicted = True
        return is_contradicted

    #I added this function for the Irale algorithm.. maybe i dont understand the algorithm well, but i guess we need it
    # This is done by the Rule.covers(ex) when the result is of the form [-1, something]
    # I add the Model.contradicts(ex) which compares if the example is contradicted by the model,
    # i.e. if there exists rules in self.rules that contradict ex
    @staticmethod
    def contradicted_ex(ex, r):
        is_contradicted = False
        sigma = Subst([], [])
        pre_match = r.prematch(ex.s, ex.a, sigma)
        post_match = r.postmatch(ex.a, ex.e, sigma)
        if len(pre_match) == 0 or len(post_match) == 0 or not r.compareSubst(pre_match[0], post_match[0]):
            is_contradicted = True
        return is_contradicted

    """
    implement the generatization for the examples using postgeneralize from Rule class.
    for all rules r in M:
   Let sigma and theta be two empty Subst
   grule=Post-Generalize(r,x,sigma,theta)
   if grule contains a generalized rule:
      Apply the reverse substitution of theta to x.s (to get gstate)
      Find a generalization gpre of grule.p and gstate using extension of sigma and theta
      Replace grule.p by gpre
      if grule is well formed and not contradicted by any memorized example :
         replace r by grule in M
if no rule could be generalized to cover x:
   Add a new rule (r.p=x.s,r.a=x.a,r.e=x.e) to M
    """
    def generalize(self, ex):
        # This list will help because we cannot change elemnt of an iterator while iterating
        add_to_model = []
        remove_from_model =[]
        generalized = False
        for i,r in enumerate(self.rules):
            sigma = Subst([], [])
            theta = Subst([], [])
            grule = r.postgeneralize(ex, sigma, theta)
            if grule:
                gstate = ex.s.revApply(theta)
                gpre = grule.s.generalizeIncOI(gstate, sigma, theta)
                grule.set_state(gpre)
                if grule.wellformed() and not self.contradicted(grule):
                    # Adds ancestor to new generalized rule:
                    grule.set_anc(r)
                    add_to_model.append(grule)
                    # Stores the index to remove from rules
                    remove_from_model.append(i)
                    generalized = True

        for elem in remove_from_model:
            self.rules.pop(elem)
        for elem in add_to_model:
            self.addRule(elem)

        if not generalized:
            new_rule = Rule(ex.s, ex.a, ex.e)
            self.addRule(new_rule)

    """
    IRALe algorithm. This function should use all the previous ones.
    I think this function has many problems
    """
    def IRALe(self, ex):
        lex = []
        specialization_done = False
        generalization_done = False
        # Don't erase: in case we need to fit the parameters in the assignment:
        #for r in self.rules:
            # if ex contradicts rule, then specialize it:
            #if r.covers(ex)[0] == -1:
            #    self.specialize2(r, ex)
            #    specialization_done = True
        specialization_done = self.specialize(ex)
        print("--------- Specialization before generalization of uncovered:")
        print(self)
        print("---------")
        if not self.covers(ex):
            generalization_done = True
            lex.append(ex)
        # Checks the uncovered examples due to specialization:
        if specialization_done:
            lex.extend(self.getUncovEx())
        for elem in lex:
            self.generalize(elem)
        if specialization_done or generalization_done:
            self.memorizeEx(ex)
