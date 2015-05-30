__author__ = 'Maira'

from OIlogic import Atom, AtomSet, Subst


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
        s += '}\n'
        return s

    def set_name(self, name):
        self.name = name


class Rule:
    def __init__(self, state, action, effect):
        self.s = state
        self.a = action
        self.e = effect
        self.name = ''
        self.anc = None

    def __str__(self):
        s = '{'
        s += 'State: '+str(self.s)+', '
        s += 'Action: '+str(self.a)+', '
        s += 'Effect: '+str(self.e)
        s += '}'
        return s

    def set_name(self, name):
        self.name = name

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
        # for ed in effect_del:
        #     present = False
        #     for s in state:
        #         present = s.__eq__(ed)
        #         if present:
        #             break
        #     if not present:
        #         return False
        #

        # rule.effect.Add intersection rule.state = empty
        if not effect_add.intersection(state):
            condition_2 = True
        else:
            condition_2 = False

        # for ea in effect_add:
        #     present = False
        #     for s in state:
        #         present = s.__eq__(ea)
        #         if present:
        #             break
        #     if present:
        #         return False
        # print("condition 2")
        action_vars = self.a.getVarSet()
        effect_vars = self.e.Add.getVarSet().union(self.e.Del.getVarSet())
        state_vars = self.s.getVarSet()


        # All vars of rule.action should occur in r.state and r.effect and r.effect may
        # refer objects/variables not occuring in r.action
        #condition_3 = action_vars.issubset(effect_vars.union(state_vars))
        diff_variables = AtomSet(list(state.difference(effect_del).union(effect_add))).getVarSet()
        condition_3 = action_vars.issubset(diff_variables)
        #for av in action_vars:
        #    if av not in effect_vars:
        #        return False
        #    if av not in state_vars:
        #        return False

        return condition_1 and condition_2 and condition_3

    """
    Return the list of substitutions R of all OI extensions theta of OI
    substitution sigma such that the rule pre-matches (gstate, gaction) with
    substitution theta.
    - (r.a)sigma = gaction
    - (r.s)sigmaTheta is contained by gstate
    """
    def prematch(self, gstate, gaction, sigma):
        if not self.a.filterOI(gaction, sigma):
            return {}
        theta = self.s.filterIncOI(gstate, sigma)
        return theta

    """
    Returns the list of substitutions R of all OI extensions theta of OI
    substitution sigma such that the rule post-matches (gstate, gaction) with
    substitution theta.
    - (r.a)invsubSigma = gaction
    - (r.e)invsubSigmaTheta = geffect
    """
    def postmatch(self, gaction, geffect, sigma):
        self.a.filterOI(gaction, sigma)
        inv = self.a.revApply(sigma)
        if not inv.filterOI(gaction, sigma):
            return {}
        effect_list = self.e.Add.toSet().union(self.e.Del.toSet())
        effect = AtomSet(effect_list)
        geffect_list = geffect.Add.toSet().union(geffect.Del.toSet())
        inv = effect.revApply(sigma)
        theta = inv.filterIncOI(AtomSet(geffect_list), sigma)
        return theta

    """
    Returns a (int, Subst) pair. If the rule coves ex, this function must return
    (1, theta) where theta is a substitution with which the rule covers ex. If ex
    contradicts the rule, this function must return (-1, theta) where theta is the
    substitution with which the rule pre-matches ex.  When both conditions do not
    occur, the function should return (0, None)
    """
    def covers(self, ex):
        pre_match = self.prematch(ex.s, ex.a, Subst([], []))
        if len(pre_match) == 0:
            return [0, None]
        else:
            post_match = self.postmatch(ex.a, ex.e, Subst([], []))
            if len(post_match) == 0:
                return [-1, pre_match]
            return [1, post_match]

    """
    Returns either None or a Rule and updates ownSubst and exSubst.
    Check gaven pseudo code.
    """
    def postgeneralize(self, ex, ownSubst, exSubst):
        return None


class Model:
    def __init__(self):
        self.rules = set()
        self.exMem = set()

    def get_rules(self):
        return self.rules

    def get_exMem(self):
        return self.exMem

    def __str__(self):
        s = 'Model:\n'
        s += '\tRules:\n'
        for r in self.rules:
            s += '\t\t'+str(r)
        s += '\tExamples Memory:\n'
        for ex in self.exMem:
            s += '\t\t'+str(ex)+'\n'
        return s

    """
    Add a new rule to the Model
    """
    def addRule(self, rule):
        self.rules.add(rule)

    """
    Memorize a new example in the Model
    """
    def memorizeEx(self, ex):
        self.exMem.add(ex)

    """
    Function that specialize a rule.
    Use the field anc and the function prematch from Rule class
    """
    def specialize(self, rule):
        return

    """
    Return a list of examples from exMem that are not covered by the Model anymore
    """
    def getUncovEx(self, rule):
        return None

    """
    Return a boolean indicating if the rule is contradicted by the Model.
    """
    def contradicted(self, rule):
        return True

    """
    implement the generatization for the examples using postgeneralize from Rule class.
    """
    def generalize(self, examples):
        return

    """
    IRALe algorithm. This function should use all the previous ones.
    """
    def IRALe(self, ex):
        lex = set()
        for r in self.rules:
            if self.contradicted(ex):
                self.specialize(r)
            for e in self.getUncovEx(r):
                lex.add(e)
        self.generalize(lex)
        #Memorize x if it triggered a revision of the theory
