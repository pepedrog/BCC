#include "acoes.h"
#include "jogo.tab.h"

struct inifunc {
  char *fname;
  fptr fnct;
};


/* Lista de verbos */
struct inifunc lfunc[] = {
  {"pegue", Pegar},
  {"tire", Tirar},
  {"coloque", Colocar},
  {"interaja", Interagir},
  {"abra", Abrir},
  {"desligue", Desligar},
  {"ligue", Ligar},
  {"estoure", Estourar},
  {"toque", Tocar},
  {"leia", Ler},
  {"atire", Atirar},
  {"fale", Falar},
  {"beba", Beber},
  {"coma", Comer},
  {"deite", Deitar},
  {"levante", Levantar},
  {"pegue", Pegar},
  {"cate", Pegar},
  {"largue", Soltar },
  {"solte", Soltar },
  {"jogue", Soltar },
  {"examine", Examinar },
  {"olhe", Examinar },
  {"veja", Examinar },
  {"quebre", Quebrar},
  {"grite", Gritar },
  {"berre", Gritar },
  {"chore", Chorar},
  {"corra", Correr},
  {"sente", Sentar},
  {0, 0}
};

/* Para objetos */
struct initobj {
  char *name;
  Elemento *obj;
};

/* Lista de objetos */
struct initobj lobjs[] = {
  {"mascara", &mascara},
  {"pessoas", &pessoas},
  {"grupo", &pessoas},
  {"quadro", &quadro},
  {"gramofone", &gramo},
  {"disco", &disco},
  {"lp", &disco},
  {"balao", &balao},
  {"bexiga", &balao},
  {"arma", &arma},
  {"revolver", &arma},
  {"pistola", &arma},
  {"cogumelos", &cogumelos},
  {"homem", &homem},
  {"velho", &homem},
  {"garrafa", &garrafa},
  {"espelho", &espelho},
  {"cama", &cama},
  {"envelope", &envelope},
  {"carta", &carta},
  {"foto", &foto},
  {"fotografia", &foto},
  {"você", &personagem},
  {"personagem", &personagem},
  {"eu", &personagem},
  { 0, 0}
};

/* Para lugares */
struct initlug {
  char *name;
  Elemento *lug;
};

/* Lista de lugares */
struct initlug llugs[] = {
  {"inicio", &sala1},
  {"audicao", &sala2},
  {"sociedade", &sala3},
  {"remanescencia", &sala4},
  {"reflexao", &sala5},
  {"hedonismo", &sala6},
  { 0, 0}
};

/* Inicializa a tabela de símbolos passada como argumento */
Lista*  init_table(Lista *sym_table) {
  int i;
  Lista *ptr = sym_table;		/* cabeça da lista */
  /* Lista de verbos */
  for (i = 0; lfunc[i].fname != 0; i++) {
	/* insere */
    ptr = LinsereGlobal(ptr, lfunc[i].fname, VERBO, lfunc[i].fnct);
	/* completa os dados */
    ptr->cabec->val = lfunc[i].fnct;
  }
  /* Lista de objetos */
  for (i = 0; lobjs[i].name != 0; i++) {
	Elemento * oo = lobjs[i].obj;
	/* insere */
    ptr = LinsereGlobal(ptr, lobjs[i].name, OBJ, oo);
	oo->conteudo = Tcria(4);
  }

  /* Lista de lugares */
  for (i = 0; llugs[i].name != 0; i++)
	/* insere */
    ptr = LinsereGlobal(ptr, llugs[i].name, LUGAR,llugs[i].lug);
  return ptr;

}
