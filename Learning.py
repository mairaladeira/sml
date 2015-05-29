__author__ = 'Maira'


class Effect:
    def __init__(self, pos, neg):
        self.Add = pos
        self.Del = neg

    def __str__(self):
        s = '{'
        s += '('+str(self.Add)+')'
        s += '('+str(self.Del)+')'
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
    def getEffect(self, prevState, newState):
        prev_atoms = prevState.toSet()
        new_atoms = newState.toSet()
        #implement the rest

    """
    Return the list of atoms of all OI extensions theta of OI substitution subst,
    such that theta.Add = other.Add and theta.Del = other.Del
    """
    def filterOI(self, other, subst):
        atoms = []
        return atoms

    #maybe new functions have to be added.


class Example:
    def __init__(self, state, action, effect):
        self.s = state
        self.a = action
        self.e = effect
        self.name = ''

    def set_name(self, name):
        self.name = name


class Rule:
    def __init__(self, state, action, effect):
        self.s = state
        self.a = action
        self.e = effect
        self.name = ''
        self.anc = None

    def set_name(self, name):
        self.name = name

    """
    This function should return true if the rule is well formed and false otherwise.
    Not necessary to check condition iii for the well formed definition
    """
    def wellformed(self):
        return True

    """
    Return the list of substitutions R of all OI extensions theta of OI
    substitution sigma such that the rule pre-matches (gstate, gaction) with
    substitution theta.
    """
    def prematch(self, gstate, gaction, sigma):
        return

    """
    Returns the list of substitutions R of all OI extensions theta of OI
    substitution sigma such that the rule post-matches (gstate, gaction) with
    substitution theta.
    """
    def postmatch(self, gstate, geffect, sigma):
        return

    """
    Returns a (int, Subst) pair. If the rule coves ex, this function must return
    (1, theta) where theta is a substitution with which the rule covers ex. If ex
    contradicts the rule, this function must return (-1, theta) where theta is the
    substitution with which the rule pre-matches ex.  When both conditions do not
    occur, the function should return (0, None)
    """
    def covers(self, ex):
        return [0, None]

    """
    Returns either None of a Rule and updates ownSubst and exSubst.
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
        s = '{'
        s += '('+str(self.rules)+'),'
        s += '('+str(self.exMem)+')'
        s += '}'
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