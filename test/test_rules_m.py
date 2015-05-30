__author__ = 'Maira'
from OIlogic import Term, Atom, AtomSet, Subst
from Learning import *
#constantes
a, b, c, floor = Term("a"), Term("b"), Term("c"), Term("floor")

#variables
X, Y, Z = Term("X"), Term("Y"), Term("Z")


# prev_state = on(a,floor),on(b,floor), on(c,a)
# new_state = on(a,floor), on(b,floor), on(c,b)
eff = Effect.getEffect(AtomSet([Atom("ON\\2", [a, floor]), Atom("ON\\2", [c, a]), Atom("ON\\2", [b, floor])]),
                       AtomSet([Atom("ON\\2", [a, floor]), Atom("ON\\2", [c, b]), Atom("ON\\2", [b, floor])])
                       )
print(eff)

# on(a,floor),on(b,floor), on(c,a) / move(c,b) / eff: on(c, b), not_on(c,a)
ex_1 = Example(
    AtomSet([Atom("ON\\2", [a, floor]), Atom("ON\\2", [c, a]), Atom("ON\\2", [b, floor])]),
    Atom("MOVE\\2", [c, b]),
    eff)

print(ex_1)

# on(X,Z) / move(X,Y) / on(X,Y), not_on(X,Z)
rule_1 = Rule(
    AtomSet([Atom("ON\\2", [X, Z])]),
    Atom("MOVE\\2", [X, Y]),
    Effect(AtomSet([Atom("ON\\2", [X, Y])]),
           AtomSet([Atom("ON\\2", [X, Z])]))
)
print(rule_1)
# check if rule is well formed
print("well formed: ", rule_1.wellformed())

s1 = Subst([], [])
#check pre-match
print('pre-match:'+str(rule_1.prematch(ex_1.s, ex_1.a, s1)[0]))
#check post-match
print('post-match:'+str(rule_1.postmatch(ex_1.a, ex_1.e, s1)[0]))
#check cover
print('cover:')
print('\ttype: '+str(rule_1.covers(ex_1)[0]))
print('\tsubst: '+str(rule_1.covers(ex_1)[1][0]))

# If we add color to the rule state, then it doesn't prematch:
rule_2 = Rule(
    AtomSet([Atom("ON\\2", [X, Z]), Atom("W\\1", [X])]),
    Atom("MOVE\\2", [X, Y]),
    Effect(AtomSet([Atom("ON\\2", [X, Y])]),
           AtomSet([Atom("ON\\2", [X, Z])]))
)
print("well formed: ",  rule_2.wellformed())
s2 = Subst([], [])
print(rule_2.prematch(ex_1.s, ex_1.a, s2))