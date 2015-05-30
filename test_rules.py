__author__ = 'humberto'
from OIlogic import Term, Atom, AtomSet, Subst
from Learning import *
#constantes
a, b, f = Term("a"),Term("b"),Term("f")

#variables
X,Y,Z = Term("X"),Term("Y"),Term("Z")


# prev_state = on(a,f),on(b,f)
# new_state = on(a,b), on(b,f)
eff = Effect.getEffect(AtomSet([Atom("ON\\2",[a,f]), Atom("ON\\2",[b,f])]),
                       AtomSet([Atom("ON\\2",[a,b]), Atom("ON\\2",[b,f])])
                       )
print(eff)

# on(a,f),on(b,f) / move(a,b) / eff: on(a, b), not_on(a,f)
ex_1 = Example(
    AtomSet([Atom("ON\\2",[a,f]), Atom("ON\\2",[b,f])]),
    Atom("MOVE\\2",[a,b]),
    eff
    )

print(ex_1)

# on(X,Z) / move(X,Y) / on(X,Y), not_on(X,Z)
rule_1 = Rule(
    AtomSet([Atom("ON\\2",[X,Z])]),
    Atom("MOVE\\2",[X,Y]),
    Effect(AtomSet([Atom("ON\\2",[X,Y])]),
           AtomSet([Atom("ON\\2",[X,Z])])
    )
)
print(rule_1)
# check if rule is well formed
print("well formed: ", rule_1.wellformed())

s1 = Subst([],[])
print(rule_1.prematch(ex_1.s, ex_1.a, s1)[0])

# If we add color to the rule state, then it doesn't prematch:
rule_2 = Rule(
    AtomSet([Atom("ON\\2",[X,Z]), Atom("W\\1",[X])]),
    Atom("MOVE\\2",[X,Y]),
    Effect(AtomSet([Atom("ON\\2",[X,Y])]),
           AtomSet([Atom("ON\\2",[X,Z])])
    )
)
print("well formed: ",  rule_2.wellformed())
s2 = Subst([],[])
print(rule_2.prematch(ex_1.s, ex_1.a, s2))