% chosing which rules would apply, if any
impossible(A,R,L,T) :- pre(F,A,R,L), time(T;T+1),not h(F,T).
possible(A,T) :- assoc(A,R,L),time(T;T+1),not impossible(A,R,L,T).
%incomplete(A,R,L,T) :- occ(A,T),pre(F,A,R,L),not h(F,T).
triggered(A,R,L,T) :- occ(A,T), assoc(A,R,L),not impossible(A,R,L,T).
overtaken(A,R,L,T) :- triggered(A,R,L,T), triggered(A,R2,L2,T),R2<R.
occ(A,R,L,T) :- triggered(A,R,L,T), not overtaken(A,R,L,T).

:-occ(A,T),not possible(A,T).

% adding new effects
h(F,T+1) :- occ(A,R,L,T), add(F,A,R,L).
% inertial rule
h(F,T+1) :- h(F,T), occ(A,R,L,T), not del(F,A,R,L).



