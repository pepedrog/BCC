#include "traduzindo.h"
#include <stdio.h>

int yyparse();

int main(){

    puts("\nBem-vindo à \n\n"
        "ooooo              .o.       ooooooooo.   oooooooooooo ooooo ooooooooo.         .o.    \n"
        "`888'             .888.      `888   `Y88. `888'     `8 `888' `888   `Y88.      .888.    \n"
        " 888             .8'888.      888   .d88'  888          888   888   .d88'     .8`888.     \n"
        " 888            .8' `888.     888ooo88P'   888oooo8     888   888ooo88P'     .8' `888.    \n"
        " 888           .88ooo8888.    888`88b.     888    '     888   888`88b.      .88ooo8888.   \n"
        " 888       o  .8'     `888.   888  `88b.   888       o  888   888  `88b.   .8'     `888.  \n"
        "o888ooooood8 o88o     o8888o o888o  o888o o888ooooood8 o888o o888o  o888o o88o     o8888o \n"
        "A Aventura de Texto feita por Bento Pereira, Daniela Favero e Pedro Gigeck.\n\n"

        "'O lar é onde o coração do homem cria raízes.' -Henrik Ibsen\n\n"

        "Dor de cabeça. Ânsia. Escuridão. Turbulência na mente. O que houve? Você não sabe. Quem é você? \n"
        "Você nem se lembra de sua identidade. Onde você está? Abra seus olhos, len-ta-men-te.\n"
        "É uma sala comum. Você não faz ideia de onde está. Você só quer ir pra casa.\n\n");

    //Criar elementos
    salas();
    insereAcoes();
	sym_table = init_table(sym_table);

	envelope.conteudo = Tcria(4);
	Tinsere(envelope.conteudo, &carta);//Coloca a carta no envelope
	
    while (yyparse() && personagem.ativo);
    return 0;
    /*
	printf("%s\n",foto.def.objeto.lista[0].quali);
	//homem.def.objeto.lista[2].val = 0;

    int online = 1;

    //Inicializa e inclui a tabela de símbolos
    //Inicializa variáveis
    //Conectar salas
    //Colocar objetos em suas posições de início (inclusive o aventureiro?)

    while(online){

		puts("--------------------------- SALA 1 - INICIO ---------------------------\n");
		atual = &sala1;
		atual->visivel = True;
		atual->conhecido = False;
		quadro.visivel = True;

        Examinar(atual, NULL);
		puts("");
        imprimeConteudo(*atual, 4);

		puts("\nVamos examinar o quadro");
		Examinar(&quadro, NULL);

		puts("\nVamos examinar a sala antes de ir embora");
		Examinar(atual, NULL);

		puts("\nVamos mover para o leste");
		Mover(&sala1, 2);

		puts("\n--------------------------- SALA 2 - AUDICAO ---------------------------\n");

		atual->visivel = True;
		atual->conhecido = False;
		gramo.visivel = True;
		balao.visivel = True;

        Examinar(atual, NULL);
		puts("");
        imprimeConteudo(*atual, 4);

		puts("\nVamos examinar o balao");
		Examinar(&balao, NULL);

		puts("\nVamos estourar o balao");
		Estourar(&balao, NULL);

		puts("\nVamos estourar o balao denovo");
		Estourar(&balao, NULL);

		puts("\nVamos examinar o gramofone");
		Examinar(&gramo, NULL);

		puts("\nVamos ligar o gramofone");
		Ligar(&gramo, NULL);

		puts("\nVamos desligar o gramofone");
		Desligar(&gramo, NULL);

		puts("\nVamos 'abrir' o gramofone");
		Abrir(&gramo, NULL);

		puts("\nVamos tirar o disco do gramofone");
		Tirar(&disco, &gramo);

		puts("\nVamos examinar o que tem na sala novamente");
		imprimeConteudo(*atual, 4);

		puts("\nVamos 'abrir' o gramofone novamente");
		Abrir(&gramo, NULL);

		puts("\nVamos colocar o disco do gramofone");
		Colocar(&disco, &gramo);

		puts("\nVamos 'abrir' o gramofone mais uma vez");
		Abrir(&gramo, NULL);

		puts("\nVamos examinar a sala antes de ir embora");
		Examinar(atual, NULL);

		puts("\nVamos mover para o Sul");
		Mover(&sala2, 2);

		puts("\n--------------------------- SALA 3 - SOCIEDADE ---------------------------\n");

		atual->visivel = True;
		atual->conhecido = False;
		pessoas.visivel = True;
		mascara.visivel = True;
		mascara.ativo = True;

		Examinar(atual, NULL);
		puts("");
        imprimeConteudo(*atual, 4);

		puts("\nVamos examinar o grupo de pessoas");
		Examinar(&pessoas, NULL);

		puts("\nVamos interagir com eles");
		Interagir(&pessoas, NULL);

		puts("\nVamos examinar a mascara");
		Examinar(&mascara, NULL);

		puts("\nVamos colocar a mascara");
		Colocar(&mascara, &personagem);

		puts("\nVerificando que mascara nao esta na sala");
		imprimeConteudo(*atual, 4);

		puts("\nVamos tentar interagir denovo");
		Interagir(&pessoas, NULL);

		puts("\nVamos tirar a mascara");
		Tirar(&mascara, NULL);

		puts("\nVamos examinar a sala antes de ir embora");
		Examinar(atual, NULL);

		puts("\n Vamos mover para o Leste");
		Mover(&sala3, 2);

		Examinar(atual, NULL);
		puts("\nParece que voltamos a sala1");
		puts("\n Vamos mover para o Sul");
		Mover(&sala1, 0);

		puts("\n--------------------------- SALA 4 - REMANESCENCIA ---------------------------\n");

		atual->visivel = True;
		atual->conhecido = False;
		envelope.visivel = True;
		envelope.ativo = True;
		foto.visivel = True;
		foto.ativo = True;

		Examinar(atual, NULL);
		puts("");
        imprimeConteudo(*atual, 4);

		puts("\nVamos examinar a foto");
		Examinar(&foto, NULL);

		puts("\nVamos examinar o evelope");
		Examinar(&envelope, NULL);

		puts("\nVamos abrir o envelope");
		Abrir(&envelope, NULL);

		puts("\nVamos tirar a carta de dentro do envelope");
		Tirar(&carta, &envelope);

		puts("\nVamos examinar a carta");
		Examinar(&carta, NULL);

		puts("\nVamos ler a carta");
		Ler(&carta, NULL);

		puts("\nVamos chorar!");
		Chorar(NULL, NULL);

		puts("\nVamos examinar a sala antes de ir embora");
		Examinar(atual, NULL);

		puts("\nVamos mover para o leste");
		Mover(&sala4, 2);

		puts("\n--------------------------- SALA 5 - REFLEXAO ---------------------------\n");

		atual->visivel = True;
		atual->conhecido = False;
		espelho.visivel = True;
		espelho.ativo = True;
		arma.visivel = True;
		arma.ativo = True;
		homem.ativo = True;
		homem.visivel = True;

		Examinar(atual, NULL);
		puts("");
        imprimeConteudo(*atual, 4);

		puts("\nVamos examinar a arma");
		Examinar(&arma, NULL);

		puts("\nVamos examinar o espelho");
		Examinar(&espelho, NULL);

		puts("\nVamos examinar o homem");
		Examinar(&homem, NULL);

		puts("\nVamos conversar algumas vezes com o homem");
		for(int i = 1; i < 5; i++){
			printf("%da vez\n", i);
			Falar(&homem, NULL);
		}

		puts("\nVamos mover para o leste, depois voltamos nessa sala");

		Mover(&sala5, 2);

		puts("\n--------------------------- SALA 6 - HEDONISMO ---------------------------\n");

		atual->visivel = True;
		atual->conhecido = False;
		cogumelos.visivel = True;
		cogumelos.ativo = True;
		garrafa.visivel = True;
		garrafa.ativo = True;
		cama.ativo = True;
		cama.visivel = True;

		Examinar(atual, NULL);
		puts("");
        imprimeConteudo(*atual, 4);

		puts("\nVamos examinar a cama");
		Examinar(&cama, NULL);

		puts("\nVamos deitar na cama");
        Deitar(&cama, NULL);

		puts("\nVamos levantar da cama");
        Levantar(&cama, NULL);

		puts("\nVamos examinar os cogumelos");
		Examinar(&espelho, NULL);

		puts("\nVamos pegar os cogumelos");
		Pegar(&cogumelos, NULL);

		puts("\nVamos come-los");
        Comer(&cogumelos, NULL);

		puts("\nVamos examinar a garrafa");
		Examinar(&garrafa, NULL);

		puts("\nVamos beber o que tem dentro");
        Beber(&garrafa, NULL);

		puts("\nVamos voltar, movendo para oeste");
		Mover(&sala6, 3);

		puts("\nHa apenas um objeto que nao interagimos ainda");
		puts("\nVamos pegar a arma...");
		Pegar(&arma,NULL);

		puts("\nVamos atirar no espelho");
		Atirar(&arma,&espelho);

		puts("\nVamos atirar no homem");
		Atirar(&arma,&homem);

		puts("\nEsgotadas as opcoes, ha apenas um jeito de acabar com esse sofrimento");
		Atirar(&arma,&personagem);

		puts("\n------------------------------------------- THE END -------------------------------------------");
		puts("-----------------------------------------------------------------------------------------------");

		online = 0;
    }
*/
}
