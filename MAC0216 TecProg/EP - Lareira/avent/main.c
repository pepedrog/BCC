#include <stdio.h>
#include "symrec.h"

int yyparse();
symrec* init_table();

int main()
{
  /* Monta o mundo */
  sym_table = init_table(sym_table);

  /* Descrição inicial */
  printf("Você está no quarto, procure examinar os lugares e objetos\n");

  /* Que comece o jogo */
  while (yyparse());
  return 0; 
}






