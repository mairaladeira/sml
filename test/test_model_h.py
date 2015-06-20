__author__ = 'humberto'

from Environment import Env
from Learning import Example, Effect, Rule, Model
from OIlogic import AtomSet, Atom, Term

a, b, c, d, floor = Term("a"), Term("b"), Term("c"), Term("d"), Term("floor")

model = Model()


#variables
X, Y, Z = Term("X"), Term("Y"), Term("Z")
# The example from the article:
r1 = Rule(
    AtomSet([Atom("w\\1",[X]), Atom("w\\1",[Y]), Atom("on\\2",[X, floor]), Atom("on\\1",[Y,floor])]),
    Atom("move\\2",[X,Y]),
    Effect(AtomSet([Atom("on\\2",[X,Y])]),
           AtomSet([Atom("on\\2",[X,floor])])
    )
)

ex1 = Example(
    AtomSet([Atom("w\\1",[a]), Atom("w\\1",[b]), Atom("on\\2",[a, floor]), Atom("on\\1",[b,floor])]),
    Atom("move\\2",[a,b]),
    Effect(AtomSet([Atom("on\\2",[a,b])]),
           AtomSet([Atom("on\\2",[a,floor])])
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

ex4 = Example(
    AtomSet([Atom("w\\1",[a]), Atom("b\\1",[c]), Atom("on\\2",[a, floor]), Atom("on\\1",[c,floor])]),
    Atom("move\\2",[a,c]),
    Effect(AtomSet([Atom("b\\1",[a])]),
           AtomSet([Atom("w\\1",[a])])
    )
)


# Example of generalization:
# model.generalize(ex1)
# model.memorizeEx(ex1)
# print(model)
# model.generalize(ex2)
# model.memorizeEx(ex2)
# print(model)
#
# print("uncovered examples: " +str(model.getUncovEx()))
#
# print("model covers ex3: "+str(model.covers(ex3)))
# print("model contradicts ex3: "+str(model.contradicts(ex3)))
#
# model.generalize(ex3)
# model.memorizeEx(ex3)
# print(model)
#
# # Test specialization:
# # new example ex4:
# print("x4 contradicts the model: "+str(model.contradicts(ex4)))
# # so we need to specialize:
# # we only have one rule, so that's the rule that is causing problems:
# model.specialize(ex4)
# model.memorizeEx(ex4)
# model.generalize(ex3)
# model.generalize(ex4)
# # Check how the rule changed as it became more specialized:
# print(model)

#################
# Same example using IRALe (comment the first example, otherwise it won't work)
model2 = Model()
model2.IRALe(ex1)
#print(model2)
model2.IRALe(ex2)
#print(model2)
model2.IRALe(ex3) # Generalizes:
print(model2)
model2.IRALe(ex4) # Specializes
print(model2)
