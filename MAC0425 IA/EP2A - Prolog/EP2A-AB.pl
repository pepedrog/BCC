%%%%% Insira aqui os seus predicados.
%%%%% Use quantos predicados auxiliares julgar necessario

% ------------------------------------ Ex 1 ------------------------------------ %

% Transforma a lista Xs em uma lista sem repeticoes Cs
lista_para_conjunto( Xs, Cs) :-
    lista_para_conjunto( Xs, [], Cs).

% lista_para_conjunto\3
% Aux eh a lista auxiliar que vai guardar os elementos unicos

% Quando acabou a lista, Aux eh o conjunto
lista_para_conjunto( [], Aux, Aux).
% Quando a cabeca X da lista ja esta em Aux
lista_para_conjunto( [X | Xs], Aux, Cs) :-
    member( X, Aux),
    lista_para_conjunto( Xs, Aux, Cs), !.
% Quando a cabeca X da lista nao esta em Aux
lista_para_conjunto( [X | Xs], Aux, Cs) :-
    append(Aux, [X], Aux2),
    lista_para_conjunto( Xs, Aux2, Cs).

% ------------------------------------ Ex 2 ------------------------------------ %

% predicado auxiliar que insere o X em Ys em todas as posicoes
% Exemplo:
% ?- insre_em_todo_lugar( x, [a, b], Ps).
%  - Ps = [x, a, b]
%  - Ps = [a, x, b]
%  - Ps = [a, b, x]

% A estrategia eh dividir o Ys na posicao e guardar a lista do
% comeco e do final
insere_em_todo_lugar( X, Ys, Ps) :-
    insere_em_todo_lugar( X, [], Ys, Ps).

% Quem realmente faz o servico, Coloca o X entre o Comeco e o Final
insere_em_todo_lugar( X, Comeco, Final, Ps) :-
    append( Comeco, [X], Comeco2),
    append( Comeco2, Final, Ps).

% Coloca um elemento do Final no Comeco e chama a recursao
insere_em_todo_lugar( X, Comeco, [Y | Ys], Ps) :-
    append( Comeco, [Y], Comeco2),
    insere_em_todo_lugar( X, Comeco2, Ys, Ps).

% Cria todas as permutacoes do primeiro argumento no segundo
mesmo_conjunto( [], []).
mesmo_conjunto( [X | Xs], Ps) :-
    mesmo_conjunto(Xs, PXs),
    insere_em_todo_lugar(X, PXs, Ps).

% ------------------------------------ Ex 3 ------------------------------------ %

uniao( Xs, Ys, Us) :-
    append( Xs, Ys, Zs),
    lista_para_conjunto( Zs, Us).

% ----------------------------------- Ex 4 ------------------------------ %

inter_conjunto( Xs, Ys, I):-
    inter_conjunto( Xs, Ys, [], I).

% Cláusula de parada, acabou o Xs então a resposta está no aux
inter_conjunto( [], _, Aux, Aux).

% Se X está em Ys, adiciopna X no Aux
inter_conjunto( [X | Xs], Ys, Aux, I) :-
    member( X, Ys),
    append( Aux, [X], Aux2),
    inter_conjunto( Xs, Ys, Aux2, I), !.
% Se X não está no Ys, só segue a recursão
inter_conjunto( [_ | Xs], Ys, Aux, I) :-
    inter_conjunto( Xs, Ys, Aux, I).


% ----------------------------------- Ex 5 ------------------------------ %

diferenca_conjunto( Xs, Ys, I):-
    diferenca_conjunto( Xs, Ys, [], I).

% Cláusula de parada, acabou o Xs então a resposta está no aux
diferenca_conjunto( [], _, Aux, Aux).

% Se X está em Ys, só segue a recursão
diferenca_conjunto( [X | Xs], Ys, Aux, I) :-
    member( X, Ys),
    diferenca_conjunto( Xs, Ys, Aux, I), !.

% Se X não está no Ys, adiciona ele no Aux
diferenca_conjunto( [X | Xs], Ys, Aux, I) :-
    append( Aux, [X], Aux2),
    diferenca_conjunto( Xs, Ys, Aux2, I), !.


%%%%%%%% Fim dos predicados adicionados
%%%%%%%% Os testes comecam aqui.
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




