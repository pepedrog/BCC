pai( mario, celia).
pai( mario, sergio).
pai( mario, selma).
pai( mario, silvio).
pai( mario, sueli).
pai( mario, angelica).

pai( leonardo, rosangela).
pai( leonardo, frederico).
pai( leonardo, arnaldo).
pai( leonardo, katia).
pai( leonardo, daniel).

pai( sergio, joao).
pai( sergio, nadia).

pai( silvio, pedro).
pai( silvio, bianca).

pai( carlos, thais).

pai( mauricio, paula).

pai( frederico, leo).
pai( frederico, tiago).
pai( tiago, heitor).

pai( arnaldo, jaqueline).
pai( arnaldo, guilherme).
pai( arnaldo, juliana).

pai( daniel, rafael).
pai( daniel, matheus).

mae( zuleide, celia).
mae( zuleide, sergio).
mae( zuleide, selma).
mae( zuleide, silvio).
mae( zuleide, sueli).
mae( zuleide, angelica).

mae( tereza, rosangela).
mae( tereza, frederico).
mae( tereza, arnaldo).
mae( tereza, katia).
mae( tereza, daniel).

mae( celia, paula).

mae( sueli, thais).

mae( idelmi, joao).
mae( idelmi, nadia).

mae( marcia, leo).
mae( marcia, tiago).
mae( thaisg, heitor).

mae( vera, jaqueline).
mae( vera, guilherme).
mae( vera, juliana).

mae( katia, pedro).
mae( katia, bianca).

mae( luciana, rafael).
mae( luciana, matheus).

progenitor( X, Y ) :- pai( X, Y ).
progenitor( X, Y ) :- mae( X, Y ).

'avô'( X, Y ) :-
	pai( X, Z ),
	progenitor( Z, Y ).

'avó'( X, Y ) :-
	mae( X, Z ),
	progenitor( Z, Y ).

avo( X, Y) :- 
    progenitor( X, Z ),
	progenitor( Z, Y ).

irmao_pai( X, Y ) :-
	pai( Z, X ),
	pai( Z, Y ),
   	X \= Y.
irmao_mae( X, Y ) :-
	mae( Z, X ),
	mae( Z, Y ),
	X \= Y.

irmao( X, Y) :-
    irmao_pai( X, Y).
irmao( X, Y) :-
    not( irmao_pai( X, Y)),
    irmao_mae( X, Y).

tio( X, Y) :-
    progenitor( PY, Y),
    irmao( PY, X).

tio_avo( X, Y) :-
    avo( VY, Y),
    irmao( VY, X).

primo( X, Y) :-
    progenitor( PX, X),
    progenitor( PY, Y),
    irmao( PX, PY),
    X \= Y.

ancestral( X, Y ) :- progenitor( X, Y ).
ancestral( X, Y ) :-
	progenitor( X, Z ),
	ancestral( Z, Y ).

ancestral_masc( X, Y) :- pai( X, Y).
ancestral_masc( X, Y) :-
    pai( X, Z),
    ancestral_masc( Z, Y).

n_avo( X, Y, N) :-
    N = 0,
    X = Y.
n_avo( X, Y, N) :-
    M is N - 1,
    progenitor(PY, Y),
    n_avo( X, PY, M).

ancestral_mais_antigo( X, Y, N) :-
    ancestral_mais_antigo(X, Y, 0, N).

ancestral_mais_antigo( X, Y, M, N) :-
    not( progenitor(_, Y)),
    X = Y,
    N is M.
ancestral_mais_antigo( X, Y, M, N) :-
    progenitor( Z, Y),
    M1 is (M + 1),
    ancestral_mais_antigo( X, Z, M1, N).

geracao( X, Y) :-
    ancestral_mais_antigo( Z, Y, N),
    n_avo( Z, X, N).

geracao_lista( Xs, Y) :-
    findall(Z, geracao( Z, Y), Zs),
    sort( Zs, Xs).

