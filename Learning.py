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
    def prematch(self, gstate, gaction, sigma):
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
    Do not use
    """
    def postmatch_old(self, gaction, geffect, sigma):
        condition_1 = True
        condition_2 = True
        ro = Subst([], [])
        # this is not necessarily true as
        # ((r.a)rho-1)sigma = a not  (r.a)rho-1 = a
        self.a.filterOI(gaction, ro)

        ro_subs = self.a.apply(ro)
        #(r.a).invro
        # you're applying ((r.a)rho)rho-1 = r.a (what's the point?)
        inv = ro_subs.revApply(ro)
        # so this is equivalent to making (r.a)sigma = a and the previous code is not making anything
        if not inv.filterOI(gaction, sigma):
            condition_1 = False
        #(r.a).invroSigma
        first_part = inv.apply(sigma)
        #condition 1: (r.a)invroSigma = gaction
        # i think this part is OK:
        if str(first_part) != str(gaction):
            condition_1 = False
        theta = self.e.filterOI(geffect, sigma)
        for t in theta:
            subs_apply_add = self.e.Add.apply(t)
            subs_apply_del = self.e.Del.apply(t)
            #Condition 2 (r.e)invroSigmaTheta = geffect
            if str(subs_apply_add) != str(geffect.Add) or str(subs_apply_del) != str(geffect.Del):
                condition_2 = False
        if condition_1 and condition_2:
            return theta
        else:
            return {}

    """
    Returns the list of substitutions R of all OI extensions theta of OI
    substitution sigma such that the rule post-matches (gstate, gaction) with
    substitution theta.
    - (r.a)invroSigma = gaction
    - (r.e)invroSigmaTheta = geffect
    """
    def postmatch(self, gaction, geffect, sigma):
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
                if not pre_match[0].__eq__(post_match[0]):
                    return [-1, pre_match]
                else:
                    return [1, post_match]


    """
    Returns either None or a Rule and updates ownSubst and exSubst.
    Check gaven pseudo code.
    if we can find a generalization gact of r.a and x.a (with sig and th):
        Find the set R of conservative generalizations of r.e.Add and  x.e.Add
                                starting from the same sig and th
        for all such generalizations gadd with subst sig' and th':
            Find a conservative generalization gdel of r.e.Del and x.e.Del
                                starting from sig' and th'
            if gdel exists (with subs sig'' and th''):
                Let gpre be the reverse application of sig'' to r.p
                grule=(gpre,gact,(gadd,gdel))
                Return grule and update sig and th to sig'' and th''

    """
    def postgeneralize(self, ex, ownSubst, exSubst):
        gact = self.a.generalize(ex.a, ownSubst, exSubst)
        if gact:
            gadd = self.e.Add.generalizeEqOI(ex.e.Add, ownSubst, exSubst)
            for g in gadd:
                sig_1 = g[1]
                th_1 = g[2]
                gdel = self.e.Del.generalizeIncOI(ex.e.Del, sig_1, th_1)
                if gdel:
                    gpre = self.s.revApply(sig_1)
                    ownSubst = sig_1
                    exSubst = th_1
                    grule = Rule(gpre, gact, Effect(g[0], gdel))
                    return grule

        else:
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
