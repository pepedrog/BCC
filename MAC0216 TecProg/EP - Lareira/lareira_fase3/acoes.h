#include "salas.h"

#define vivo 0
#define atirou 1
#define conversas 2
#define deitado 3

int imprimeConteudo(Elemento, int , char);
//Imprime a compartimento->conteudo, uma TabSim da struct Elemento

int Mover(Elemento*, int);

int Examinar(Elemento*, Elemento*);
//Imprime a descrição longa do objeto examinado (e1), se ja for conhecido, imprime a descricao curta

int Tirar(Elemento*, Elemento*);
//Retira a máscara (e1) do personagem (e2)

int Colocar(Elemento*, Elemento*);
//Coloca a máscara (e1) do personagem (e2)
//Permite o uso da função Interagir

int Interagir(Elemento*, Elemento*);
//Interage com o grupo de pessoas da sala 3
//Essa função só ocorre se a máscara estiver colocada (pela função Colocar)

int Abrir(Elemento*, Elemento*);
//Imprime o conteúdo de e1

int Desligar(Elemento*, Elemento*);
//Desliga o gramofone (e1), o que não gera efeitos reais pois essa é a intenção do jogo :-)

int Ligar(Elemento*, Elemento*);
//Assim como desligar o gramofone é inútil, ligar também é

int Estourar(Elemento*, Elemento*);
//Torna o balão inativo

int Tocar(Elemento*, Elemento*);
//Coloca o disco no gramofone

int Ler(Elemento*, Elemento*);
//Imprime a mensagem na carta (e1)

int Atirar(Elemento*, Elemento*);
//Atira usando a arma (e1) e o efeito causado depende do alvo (e2) do tiro

int Falar(Elemento*, Elemento*);
//Conversa com o homem da sala 5

int Beber(Elemento*, Elemento*);
//Consome o líquido da garrafa, mas o líquido é infinito! (De novo é parte do conceito da nossa aventura)

int Comer(Elemento*, Elemento*);
//Consome o cogumelo (e1), novamente um elemento infinito

int Deitar(Elemento*, Elemento*);
//Deitar-se na cama (e1) altera o atributo "deitado"

int Levantar(Elemento*, Elemento*);
//Levantar-se na cama (e1) altera o atributo "deitado"

int Pegar(Elemento*, Elemento*);
//Pegar um elemento (e1) e adicioná-lo ao conteúdo do personagem (e2)

int Soltar(Elemento*, Elemento*);
//Remover um elemento (e1) do conteúdo do personagem (e2)

int Quebrar(Elemento*, Elemento*);
//Torna e1 inativo

int Gritar(Elemento*, Elemento*);
//Imprime uma mensagem

int Chorar(Elemento*, Elemento*);
//Imprime uma mensagem

int Sentar(Elemento*, Elemento*);
//Imprime uma mensagem

int Correr(Elemento*, Elemento*);
//Imprime uma mensagem

void insereAcoes();
//Insere as funçãoes de ações nos respectivos objetos
