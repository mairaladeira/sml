__author__ = 'Maira'
from OIlogic import Term, Atom, AtomSet, Subst
from Learning import *
#constantes
a, b, c, d, floor = Term("a"), Term("b"), Term("c"), Term("d"), Term("floor")

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
#print('post-match2:'+str(rule_1.postmatch2(ex_1.a, ex_1.e, s1)[0]))
#check cover
print('cover:')
print('\ttype: '+str(rule_1.covers(ex_1)[0]))
print('\tsubst: '+str(rule_1.covers(ex_1)[1][0]))

# If we add color to the rule state, then it doesn't prematch:
rule_2 = Rule(
    AtomSet([Atom("w\\1", [X]), Atom("W\\1", [Y]), Atom("ON\\2", [X, floor]), Atom("ON\\2", [Y, floor])]),
    Atom("MOVE\\2", [X, Y]),
    Effect(AtomSet([Atom("ON\\2", [X, Y])]),
           AtomSet([Atom("ON\\2", [X, floor])]))
)
eff2 = Effect.getEffect(AtomSet([Atom("ON\\2", [c, d])]),
                        AtomSet([Atom("ON\\2", [c, floor])])
                        )

ex_2 = Example(
    AtomSet([Atom("B\\1", [c]), Atom("B\\1", [d]), Atom("ON\\2", [c, floor]), Atom("ON\\2", [d, floor])]),
    Atom("MOVE\\2", [c, d]),
    eff2)

s2 = Subst([], [])
s3 = Subst([], [])
if rule_2.wellformed():
    print('Rule: '+str(rule_2))
    print('Example: '+str(ex_1))
    print('post-generalization: '+str(rule_2.postgeneralize(ex_1, s2, s3)))
    print('Substitution 1: '+str(s2))
    print('Substitution 2: '+str(s3))
    new_rule = rule_2.postgeneralize(ex_1, s2, s3)

# The example from the article:
r1 = Rule(
    AtomSet([Atom("w\\1",[X]), Atom("w\\1",[Y]), Atom("on\\2",[X, floor]), Atom("on\\1",[Y,floor])]),
    Atom("move\\2",[X,Y]),
    Effect(AtomSet([Atom("on\\2",[X,Y])]),
           AtomSet([Atom("on\\2",[X,floor])])
    )
)
ex2 = Example(
    AtomSet([Atom("w\\1",[b]), Atom("w\\1",[a]), Atom("on\\2",[b, floor]), Atom("on\\1",[a,floor])]),
    Atom("move\\2",[b,a]),
    Effect(AtomSet([Atom("on\\2",[b,a])]),
           AtomSet([Atom("on\\2",[b,floor])])
    )
)
ex3 = Example(
    AtomSet([Atom("b\\1",[c]), Atom("b\\1",[d]), Atom("on\\2",[c, floor]), Atom("on\\1",[d,floor])]),
    Atom("move\\2",[c,d]),
    Effect(AtomSet([Atom("on\\2",[c,d])]),
           AtomSet([Atom("on\\2",[c,floor])])
    )
)

print('cover:')
print('\ttype: '+str(r1.covers(ex2)[0]))
print('\tsubst: '+str(r1.covers(ex2)[1][0]))
print('cover:')
print('\ttype: '+str(r1.covers(ex3)[0]))
#print('\tsubst: '+str(r1.covers(ex3)[1][0]))