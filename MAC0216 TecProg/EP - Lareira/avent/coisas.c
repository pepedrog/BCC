#include <stdio.h>
#include <stdlib.h>
#include "symrec.h"
#include "coisas.h"
#include "avent.tab.h"

/* Variáveis globais */
symrec *sym_table  = (symrec *) 0; /* Tabela de símbolos global */
symrec *inventario = (symrec *) 0; /* material com o aventureiro */
Elemento *Posic    = (Elemento *) 0; /* Posição atual */

/* Objetos  */
Elemento fogo    = {"fogo",   "É uma chama quente e bruxuleante", "uma chama", NULL, OBJ, .Det.obj={1,1}};
Elemento gelo    = {"gelo",   "É um pedaço de gelo bem frio", "uma pedra de gelo", NULL, OBJ, .Det.obj={1, 1}};
Elemento vapor   = {"vapor",   "Parece fumaça, dança ao vento", "simplesmente vapor", NULL, OBJ, .Det.obj={0,0}};
Elemento lepre   = {"leprechaum", "Um leprechaum perdido, vindo da Irlanda, seu nome é Kirkpatrick", "um homenzinho mal encarado", NULL, OBJ, .Det.obj={ 1,1}};
Elemento caneta  = {"caneta", "Uma caneta vermelha, ótima para corrigir provas", "uma caneta vermelha", NULL, OBJ, .Det.obj={0,0}};
Elemento lapis   = {"lapis",  "Um lápis azul, não serve para muitas coisas", "um lapis azul", NULL, OBJ, .Det.obj={1,1}};
Elemento hamster = {"hamster","Um roedor bonitinho, parece muito assustado.", "um hamster fofinho", NULL, OBJ, .Det.obj={1,1}};
Elemento prova   = {"prova",  "Uma prova cheia de garranchos e de escrita insegura", "uma prova escrabosa", NULL, OBJ, .Det.obj={1,1}};

/* Lugares */
Elemento sala   = {"sala", "um pequeno escritório de trabalho", "sala pequena", NULL, LUGAR, .Det.lug.Saidas =  {NULL, NULL, NULL, NULL, NULL,NULL}};
Elemento quarto = {"quarto", "um grande quarto bagunçado", "quarto enorme", NULL, LUGAR, .Det.lug.Saidas =  {NULL, NULL, &sala, NULL, &sala, NULL}};

//
// Funções auxiliares
//

/* verifica se um objeto está presente e visível */
/* retorna 1 se no local, 2 se no inventário, 0 se não existir*/
int presente(char *nome) {
  /* inventário? */
  if (getsym(inventario, nome)) return 2;
  if (getsym(Posic->cont, nome)) return 1;
  return 0;
}

/* Implementações dos verbos */

/* Macros para testar propriedades comuns */
#define Ativo(x) (x)->Det.obj.ativo
#define Visivel(x) (x)->Det.obj.visivel

/* Transfere um elemento para o inventário */
void Pegar(Elemento *o1, Elemento *o2) {
  if (o1->tipo == LUGAR) {
	puts("Não dá para pegar um lugar!");
	return;
  }

  if (Ativo(o1)) {
	if (Visivel(o1)) {
	  int r = presente(o1->nome);
	  switch (r) {
	  case 2:
		printf("Você já está com %s!\n", o1->nome);
		  return;
	  case 1:
		/* retira do local */
		Posic->cont = popsym(Posic->cont, o1->nome);
		/* insere no inventário */
		inventario = putsym(inventario, o1->nome, OBJ,o1);
		printf("Peguei %s\n", o1->nome);
		return;
	  default:
		printf("Não há %s aqui!\n", o1->nome);
		return;
	  }
	}
	printf("Não consigo ver nenhum %s!\n", o1->nome);
  }
  else
	printf("Não existe %s!!!!\n", o1->nome);
}

/* Transfere do inventário para o local atual */
void Largar(Elemento *o1, Elemento *o2) {
  if (o1->tipo == LUGAR) {
	puts("Largue a mão de ser besta!");
	return;
  }
  if (getsym(inventario, o1->nome)) {
	/* retira do inventario */
	inventario = popsym(inventario, o1->nome);

	/* insere no local */
	Posic->cont = putsym(Posic->cont, o1->nome, OBJ,o1);
	return;
  }
  else {
	/* Em inglês for fun */
	puts("You don't have it");
  }
}

/* Descreve um Elemento em detalhes */
void Examinar(Elemento *o1, Elemento *o2) {
  symrec *ptr;

  /* o default é descrever o local atual */
  if (o1 == NULL || o1 == Posic) {
	puts(Posic->longa);
	puts("Aqui tem:");
	for (ptr = Posic->cont; ptr != (symrec *) 0;
		 ptr = (symrec *)ptr->next) {
	  /* como a lista contém tods os nomes, precisamos filtrar */
	  if (ptr->tipo == OBJ) {
		Elemento *oo = (Elemento *)ptr->value;
		if (Visivel(oo)  && Ativo(oo))
		  printf("\t%s\n", oo->nome);
	  }
	}
	return;
  }
  if (o1->tipo == OBJ)
	if (Ativo(o1) && Visivel(o1))
	  puts(o1->longa);
	else puts("Oi?");
  else
	puts("Não tenho como responder neste momento");
}

/* descrição curta de um elemento, está incompleta */
void Olhar(Elemento *o1, Elemento *o2) {
  if (o1) 
	puts(o1->curta);
  else
	puts(Posic->curta);
}

void Gritar(Elemento *o1, Elemento *o2){
  puts("YEEAAAAAOOOOOWWWGRRUWL");
}

/* Estas duas funções são mais sofisticadas, pois alteram outros elementos */
void PegarGelo(Elemento *o1, Elemento *o2) {
  if (presente("gelo")) { 
	if (getsym(inventario, "fogo")) {
	  inventario = popsym(inventario, "fogo");
	  Posic->cont = popsym(Posic->cont, "gelo");
	  Posic->cont = putsym(Posic->cont, "vapor", OBJ, &vapor);
	  vapor.Det.obj = (Objeto) {1,1};
	  puts("O gelo e o fogo se fundiram...");
	  return;
	}
	else {
	  puts("BRRRrr, que frio, mas eu aguento");
	}
  }
  Pegar(&gelo, NULL);
}

void PegarFogo(Elemento *o1, Elemento *o2) {
  if (presente("fogo")) { 
	if (getsym(inventario, "gelo")) {
	  inventario = popsym(inventario, "gelo");
	  Posic->cont = popsym(Posic->cont, "fogo");
	  Posic->cont = putsym(Posic->cont, "vapor", OBJ, &vapor);
	  vapor.Det.obj = (Objeto) {1,1};
	  puts("O fogo e o gelo se fundiram...");
	  return;
	}
	else {
	  puts("UAU! AII! ARRGGHH! Que quente, mas eu aguento");
	}
  }
  Pegar(&fogo, NULL);
}

/* exemplo comportamento especial */
void PegarVapor(Elemento *o1, Elemento *o2) {
  if (Visivel(o1))
	puts("Não dá! É muito etéreo...");
  else
	Pegar(&vapor,NULL);
}

/* Libera mais um elemento */
void JogarLeprechaum(Elemento *o1, Elemento *o2) {
  puts("Kirkpatrick emite umas palavras impronunciáveis num jogo de respeito\n"
	   "Algo como %@!#$@!&");
  if (!Ativo(&caneta)) {
	caneta.Det.obj = (Objeto) {1,1};
	puts("Ele deixou cair alguma coisa!");
  }
  Largar(&lepre, NULL);
}

/* outro comportamento especial */
void JogarHamster(Elemento *o1, Elemento *o2) {
  printf("O %s se agarra desesperadamente a você e é impossível largá-lo!\n", o1->nome);
}

void Corrigir(Elemento *o1, Elemento *o2) {
  int r;
  if ((r = presente(o1->nome)))
	puts("Dei-lhe uma dura!");
  else printf("Corrigir o quê? Não vejo %s\n", o1->nome);
}

void CorrigirProva(Elemento *o1, Elemento *o2) {
  if (!getsym(inventario, "prova"))
	puts("Não estou com a prova...");
  else if (!getsym(inventario, "caneta"))
	puts("preciso da ferramenta correta para  a correção!");
  else {
	puts("Pronto! Missão cumprida!\n"
		 "A prova está corrigida, mas é melhor você não saber o resultado...\n"
		 "*** FIM ***");
	exit(0);
  }
}

/* comportamento especial que depende do lugar */
void GritaQuarto(Elemento *o1, Elemento *o2) {
  puts("Psiuuuu!!!\nIsto é um quarto!!!!");
}


/* Para inicializar as funções, copiei da calculadora */
struct initfunc {
  char *fname;
  Fptr fnct;
};

/* Lista de verbos */
struct initfunc lfunc[] = {
  {"pegue", Pegar},
  {"cate", Pegar},
  {"largue", Largar },
  {"solte", Largar },
  {"jogue", Largar },
  {"examine", Examinar },
  {"olhe", Olhar },
  {"veja", Olhar },
  {"grite", Gritar },
  {"berre", Gritar },
  {"corrija", Corrigir },
  {0, 0}
};

/* Para objetos */
struct initobj {
  char *name;
  Elemento *obj;
};

/* Lista de objetos */
struct initobj lobjs[] = {
  {"fogo",  &fogo},
  {"gelo",  &gelo},
  {"leprechaum", &lepre},
  {"Kirkpatrick", &lepre},
  {"lapis", &lapis},
  {"caneta", &caneta},
  {"hamster", &hamster},
  {"prova", &prova},
  {"vapor", &vapor},
  { 0, 0}
};

/* Para lugares */
struct initlug {
  char *name;
  Elemento *lug;
};

/* Lista de lugares */
struct initlug llugs[] = {
  {"quarto",  &quarto},
  {"sala",    &sala},
  { 0, 0}
};

/* Inicializa a tabela de símbolos passada como argumento */
symrec*  init_table(symrec *sym_table)
{
  int i;
  symrec *ptr = sym_table;		/* cabeça da lista */
  /* Lista de verbos */
  for (i = 0; lfunc[i].fname != 0; i++) {
	/* insere */
    ptr = putsym(ptr, lfunc[i].fname, VERBO, lfunc[i].fnct);
	/* completa os dados */
    ptr->value = lfunc[i].fnct;
  }
  /* Lista de objetos */
  for (i = 0; lobjs[i].name != 0; i++) {
	Elemento * oo = lobjs[i].obj;
	/* insere */
    ptr = putsym(ptr, lobjs[i].name, OBJ, oo);
	oo->cont = NULL;
  }

  /* Lista de lugares */
  for (i = 0; llugs[i].name != 0; i++) 
	/* insere */
    ptr = putsym(ptr, llugs[i].name, LUGAR,llugs[i].lug);

  /* Coloca os objetos nos lugares */
  quarto.cont = putsym(quarto.cont, "fogo",       OBJ, &fogo);
  quarto.cont = putsym(quarto.cont, "gelo",       OBJ, &gelo);
  quarto.cont = putsym(quarto.cont, "leprechaum", OBJ, &lepre);
  quarto.cont = putsym(quarto.cont, "lapis",  	  OBJ, &lapis);
  quarto.cont = putsym(quarto.cont, "caneta", 	  OBJ, &caneta);

  sala.cont = putsym(sala.cont, "prova",   OBJ, &prova);
  sala.cont = putsym(sala.cont, "hamster", OBJ, &hamster);

  /* coloca as saídas da sala, o quarto já tem */
  sala.Det.lug.Saidas[3] = &quarto;

  /* Ajustes finais */
  gelo.cont=    putsym(gelo.cont,    "pegue",   VERBO, PegarGelo);
  fogo.cont=    putsym(fogo.cont,    "pegue",   VERBO, PegarFogo);
  lepre.cont=   putsym(lepre.cont,   "jogue",   VERBO, JogarLeprechaum);
  hamster.cont= putsym(hamster.cont, "jogue",   VERBO, JogarHamster);
  quarto.cont=  putsym(quarto.cont,  "grite",   VERBO, GritaQuarto);
  vapor.cont=   putsym(vapor.cont,   "pegue",   VERBO, PegarVapor);
  prova.cont=   putsym(prova.cont,   "corrija", VERBO, CorrigirProva);

  Posic = &quarto;
  /* retorna a nova cabeça da lista */
  return ptr;
}

