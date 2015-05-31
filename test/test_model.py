__author__ = 'Maira'
from Environment import Env
from Learning import Example, Effect
from OIlogic import AtomSet, Atom, Term

env = Env(4)
model = env.get_model()
state = env.generateState()
actions = env.getAllActions()
a, b, c, d, floor = Term('a'), Term('b'), Term('c'), Term('d'), Term('floor')
ex_1 = Example(state, actions[1], Effect(AtomSet([Atom("ON\\2", [a, b])]), AtomSet([Atom("ON\\2", [a, floor])])))
ex_2 = Example(state, actions[11], Effect(AtomSet([Atom("ON\\2", [c, d])]), AtomSet([Atom("ON\\2", [c, floor])])))

print(ex_1)
print(ex_2)

model.memorizeEx(ex_1)
model.memorizeEx(ex_2)

print(model)
rules = model.get_rules()
for r in rules:
    s = model.specialize(r)
    print(s)
    uex = model.getUncovEx(r)
    print('Examples:')
    for e in uex:
        print('\t'+str(e))
    c = model.contradicted(r)
    print(c)
exs = model.get_exMem()
model.generalize(exs)
print('---------')
print(model)
for e in exs:
    model.IRALe(e)
    print(model)
    print('--')