%%%%% Insira aqui os seus predicados.
%%%%% Use quantos predicados auxiliares julgar necessário







%%%%%%%% Fim dos predicados adicionados
%%%%%%%% Os testes começam aqui.
%%%%%%%% Para executar os testes, use a consulta:   ?- run_tests.

%%%%%%%% Mais informacoes sobre testes podem ser encontradas em:
%%%%%%%%    https://www.swi-prolog.org/pldoc/package/plunit.html

:- begin_tests(conjuntos).
test(lista_para_conjunto, all(Xs=[[1,a,3,4]]) ) :-
    lista_para_conjunto([1,a,3,3,a,1,4], Xs).
test(lista_para_conjunto2,fail) :-
    lista_para_conjunto([1,a,3,3,a,1,4], [a,1,3,4]).

test(mesmo_conjunto, set(Xs=[[1,a,3],[1,3,a],[a,1,3],[a,3,1],[3,a,1],[3,1,a]])) :-
    mesmo_conjunto([1,a,3], Xs).
test(uniao_conjunto2,fail) :-
    mesmo_conjunto([1,a,3,4], [1,3,4]).

test(uniao_conjunto, set(Ys==[[1,a,3],[1,3,a],[a,1,3],[a,3,1],[3,a,1],[3,1,a]])) :-
    uniao_conjunto([1,a], [a,3], Xs),
    mesmo_conjunto(Xs,Ys).
test(uniao_conjunto2,fail) :-
    uniao_conjunto([1,a,3,4], [1,2,3,4], [1,1,a,2,3,3,4,4]).

test(inter_conjunto, all(Xs==[[1,3,4]])) :-
    inter_conjunto([1,a,3,4], [1,2,3,4], Xs).
test(inter_conjunto2,fail) :-
    inter_conjunto([1,a,3,4], [1,2,3,4], [1,1,3,3,4,4]).

test(diferenca_conjunto, all(Xs==[[2]])) :-
    diferenca_conjunto([1,2,3], [3,a,1], Xs).
test(diferenca_conjunto2,fail) :-
    diferenca_conjunto([1,3,4], [1,2,3,4], [_|_]).

:- end_tests(conjuntos).
