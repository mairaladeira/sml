__author__ = 'humberto'
from OIlogic import Term, Atom, AtomSet, Subst
from Learning import Effect

# Substitutions
#constantes
t1,t2,t3,t4=Term("t1"),Term("t2"),Term("t3"),Term("t4")
#variables
X,Y,Z,U,W=Term("X"),Term("Y"),Term("Z"),Term("U"),Term("W")
#atoms

s1,s2,s3=Subst([],[]),Subst([],[]), Subst([],[])

#variables
a1 = Atom("P\\3",[X,Z,t3])
a2 = Atom("Q\\2",[U,Y])
a3 = Atom("P\\2",[X, W])

b1 = Atom("P\\3",[t1,Z,t3])
b2 = Atom("Q\\2",[t2,Y])
b3 = Atom("P\\2", [X,t4])

as1 = AtomSet([a1,a2, a3])
as2 = AtomSet([a3])
bs1 = AtomSet([b1,b2,b3])

# This re examples or unifications (filterings) the s variable give the substitution used:
print(a1.filterOI(b1,s1))
print(s1)
print(a2.filterOI(b2,s2))
print(s2)

# This is a kind of substitution that applies for a set of atoms and is called extensions:
# (see the SUBSOMPTION section of the homework)
kk = as1.filterIncOI(bs1)
print(kk[0])

