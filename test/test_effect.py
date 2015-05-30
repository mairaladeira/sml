__author__ = 'humberto'

from OIlogic import Term, Atom, AtomSet, Subst
from Learning import Effect

#constantes
t1, t2, t3 = Term("t1"), Term("t2"), Term("t3")
#variables
X, Y, Z, U = Term("X"), Term("Y"), Term("Z"), Term("U")
#atoms
a1 = Atom("P\\2", [X, Y])
a2 = Atom("Q\\2", [X, Y])
a3 = Atom("P\\2", [U, Y])
a4 = Atom("Q\\2", [Z, Y])

b1 = Atom("P\\2", [X, Y])
b2 = Atom("P\\2", [X, X])
b3 = Atom("P\\2", [Y, U])
b4 = Atom("P\\2", [Z, Y])
s1, s2 = Subst([], []), Subst([], [])

prev = AtomSet([a1, a2, a3, a4])
new = AtomSet([b1, b2, b3, b4])

ef = Effect.getEffect(prev, new)
print(ef)

filt_ef = ef.filterOI(ef)
print(filt_ef[0])





