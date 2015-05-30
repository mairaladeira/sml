import random


class Subst:
    def __init__(self, lvars=[], lconst=[]):
        self.vars = lvars
        self.vals = lconst
        self.forbidVal = []

    def valOfVar(self, var):
        if var in self.vars:
            ind = self.vars.index(var)
            return self.vals[ind]
        return False

    def isAttributed(self,val):
        return val in self.vals

    def hasAttribution(self,var):
        return var in self.vars


    def varForVal(self,val):
        if val in self.vals:
            ind=self.vals.index(val)
            return self.vars[ind]
        if val.isVar():
            return val
        return Term.newVar()

    def affectOI(self,var,val):
        if var in self.vars:
            return val == self.valOfVar(var)
        if (val in self.vals) or (val in self.forbidVal) or (var in self.vals) or (var in self.forbidVal) or (val in self.vars):
        # a=(val in self.vals)
        # b=(val in self.forbidVal)
        # c=(val in self.vars)
        # d=(var in self.forbidVal)
        # print "Var",var,"-> Val",val,"in s",self," : Echec. val in vals ",a,"val forbid",b,"var in vals",c,"varforbid", d
            return False
        self.vars.append(var)
        self.vals.append(val)
        return True

    def forbidValue(self,c):
        if c in self.vals:
            return False
        if not(c in self.forbidVal):
            self.forbidVal.append(c)
        return True

    def __add__(self,other):
        s = self.copy()
        for i,var in enumerate(other.vars):
            if (not (s.affectOI(var, other.vals[i]))):
                continue
        return s

    def copy(self):
        s = Subst([],[])
        for c in self.forbidVal:
            s.forbidValue(c)
        for i, var in enumerate(self.vars):
            s.affectOI(var, self.vals[i])
        return s

    def setTo(self,other):
        self.vars = []
        self.vals = []
        self.forbidVal = []
        for c in other.forbidVal:
            self.forbidValue(c)
        for i,var in enumerate(other.vars):
            self.affectOI(var,other.vals[i])

    def __str__(self):
        s = "{ "
        for i, var in enumerate(self.vars):
            s = s + "(" + str(var) + "\\" + str(self.vals[i]) + ") "
        for v in self.forbidVal:
            s += "-"+str(v)
        s += "}"

        return s


class Term:
    lastVarIndex=0

    def __init__(self, name):
        self.name = name
        self.var = name[0].isupper() # TRUE if term is a variable

    def __eq__(self, t):
        return isinstance(t, Term) and self.name == t.name

    def __hash__(self):
        return hash(self.name)

    def isVar(self):
        return self.var

    def __str__(self):
        return self.name

    @staticmethod
    def newVar():
        Term.lastVarIndex += 1
        #print "newVar : Var",Term.lastVarIndex
        return Term("Var" + str(Term.lastVarIndex))

    def filterOI(self, other, s=Subst([],[])):
        if self.isVar():
            if other.isVar():
                return self.__eq__(other)
            return s.affectOI(self, other)
        else:
            return s.forbidValue(self) and self == other
        #return False

    def generalize(self, other, s=Subst([], []), s2=Subst([],[])):
        #  if self.__eq__(other):
        #     if s.forbidValue(self) and s2.forbidValue(other):
        #       return self
          #   print "Forbidden value ","self",self,"s",s,"other",other,"so",s2
        #     return None
        if s.isAttributed(self):
            gen = s.varForVal(self)
        elif s2.isAttributed(other):
            gen = s2.varForVal(other)
        elif (self.isVar()) or (self == other):
            gen = self
        elif other.isVar():
            gen = other
        else:
            gen = Term.newVar()
        # selfOk1=(gen==self and s.forbidValue(self))
        # selfOk2=selfOk1 or s.affectOI(gen,self)
        # otherOk1=(gen==other and s2.forbidValue(other))
        # otherOk2=otherOk1 or s2.affectOI(gen,other)
        if ((gen == self and s.forbidValue(self)) or s.affectOI(gen,self)) and ((gen == other and s2.forbidValue(other)) or s2.affectOI(gen, other)):
            return gen
    #   print "Echec gen",gen,"sOk",selfOk1,selfOk2,"oOk",otherOk1,otherOk2," self",self,"s",s,"other",other,"so",s2
        return None

    def apply(self, subs):
        if self.isVar():
            if self in subs.vars:
                ind = subs.vars.index(self)
                return subs.vals[ind]
        return self

    def revApply(self, subs):
        if self in subs.vals:
            ind = subs.vals.index(self)
            return subs.vars[ind]
        return self


class Signature:
    def __init__(self, name, arity=0):
        self.name = name
        self.arity = arity

    def __eq__(self, s):
        return (self.arity == s.arity) and (self.name == s.name)


class Atom:
    def __init__(self, atom, L_args):
        if isinstance(atom, Signature):
            self.sig = atom
        elif isinstance(atom, str):
            s = atom.split('\\')
            self.sig = Signature(s[0], int(s[1]))
        self.args = L_args

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, a):
        return isinstance(a, Atom) and str(self) == str(a)

    @staticmethod
    def parse(name):
        elts = name.split("(")
        pred = elts[0].strip()
        if len(elts) <= 1:
            return Atom(pred+"\\0", [])
        args = elts[1][:-1].split(",")
        pred = pred + "\\" + str(len(args))
        L_args = []
        for arg in args:
            L_args.append(Term(arg.strip()))
        return Atom(pred, L_args)

    def unifyOI(self, other, s=Subst([], [])):
        if not(self.sig.__eq__(other.sig)):
            #print "Signature differente"
            return False
        for i, arg in enumerate(self.args):
            if not(arg.unifyOI(other.args[i],s)):
                #print "Echec a l'argument ", i
                return False
        return True

    def filterOI(self, other, s=Subst([],[])):
        if not(self.sig.__eq__(other.sig)):
            #print "Signature differente"
            return False
        for i, arg in enumerate(self.args):
            if not(arg.filterOI(other.args[i],s)):
                #print "Echec a l'argument ", i," : ",arg,"!=",other.args[i]
                return False
        return True

    def generalize(self, other, ownSubst=Subst([],[]), otherSubst=Subst([],[])):
        if not(self.sig.__eq__(other.sig)):
            #print "Signature differente"
            return None
        LArgs = []
        cs1 = ownSubst.copy()
        cs2 = otherSubst.copy()
        for i, arg in enumerate(self.args):
            arg2 = other.args[i]
            tg = arg.generalize(arg2,ownSubst,otherSubst)
            if tg == None:
                #ownSubst.setTo(cs1)
                #otherSubst.setTo(cs2)
                return None
            LArgs.append(tg)
        return Atom(self.sig, LArgs)

    def __str__(self):
        s = self.sig.name
        if self.sig.arity > 0:
            s = s+"("
            for arg in self.args[:-1]:
                s = s+str(arg)+", "
            s = s+str(self.args[-1])+")"
        return s

    def getArgSet(self):
        return set(self.args)

    def getVarSet(self):
        res = set()
        for t in self.args:
            if t.isVar():
                res.add(t)
        return res

    def apply(self,subs):
        L_args = []
        for arg in self.args:
            L_args.append(arg.apply(subs))
        return Atom(self.sig, L_args)

    def revApply(self, subs):
        L_args = []
        for arg in self.args:
            L_args.append(arg.revApply(subs))
        return Atom(self.sig,L_args)


class AtomSet:
    def __init__(self, L_atoms=[]):
        self.set=L_atoms

    def __str__(self):
        s = "["
        for i, atom in enumerate(self.set):
            s += str(atom)
            if i < len(self.set)-1:
                s += ", "
        s += "]"
        return s

    def toSet(self):
        return set(self.set)

    def restrict(self,i):
        res = AtomSet([])
        res.set = self.set[i:]
        return res

    def apply(self, subs):
        L = []
        for atom in self.set:
            L.append(atom.apply(subs))
        return AtomSet(L)

    def revApply(self, subs):
        L = []
        for atom in self.set:
            L.append(atom.revApply(subs))
        return AtomSet(L)

    def filterIncOI(self, other, s=Subst([], [])):
        if self.set == []:
            return [s]
        atom = self.set[0]
        res = []
        for at2 in other.set:
            s2 = s.copy()
            #print "Filter ",atom," with ",at2," (",s2,")"
            if atom.filterOI(at2,s2):
                r2 = self.restrict(1).filterIncOI(other,s2)
                res += r2
        return res

    def generalizeEqOI(self, other, s1, s2):
        gen = AtomSet([])
        if len(self) != len(other):
            return []
        res = self.generalizeEqOIrec(other, gen, s1, s2)
        return res

    def generalizeEqOIrec(self, other, gen, s1, s2):
        #print "deb with ", self," and ",other, "( gen = ",gen,",",s1,",",s1,")"
        if self.set == []:
            #print "return (",gen,",",s1,",",s2,")"
            return [(gen, s1, s2)]
        L1 = self.set[:]
        random.shuffle(L1)
        el1 = L1[0]
        L2 = other.set[:]
        random.shuffle(L2)
        res = []
        #print "recherche pour ",el1
        for el2 in L2:
            grec = AtomSet(gen.set[:])
            ts1 = s1.copy()
            ts2 = s2.copy()
            #print "   test el2: ",el2
            g=el1.generalize(el2,ts1,ts2)
            #print "   gen : g=",g
            if g != None:
                grec.set.append(g)
                L2r = L2[:]
                L2r.remove(el2)
                L2AS = AtomSet(L2r)
                r2 = AtomSet(L1[1:]).generalizeEqOIrec(L2AS,grec,ts1,ts2)
                #"   Obtained r2 : ",
                #for (a,b,c) in r2:
                    #print "              (",a,",",b,",",c,")"
                res += r2
        return res

    def generalizeIncOI(self, other, ownSubst=Subst([],[]), otherSubst=Subst([],[])):
        L1 = self.set[:]
        L2 = other.set[:]
        gen = AtomSet([])
        while len(L1) > 0 and len(L2) > 0:
            el1 = random.choice(L1)
            random.shuffle(L2)
            for el2 in L2:
                s1 = ownSubst.copy()
                s2 = otherSubst.copy()
                g = el1.generalize(el2,s1,s2)
                if g != None:
                    gen.set.append(g)
                    ownSubst.setTo(s1)
                    otherSubst.setTo(s2)
                    L2.remove(el2)
                    break
            L1.remove(el1)
        return gen

    def __len__(self):
        return len(self.set)

    def getArgSet(self):
        res = set()
        for atom in self.set:
            res |= atom.getArgSet()
        return res

    def getVarSet(self):
        res = set()
        for atom in self.set:
            res |= atom.getVarSet()
        return res


