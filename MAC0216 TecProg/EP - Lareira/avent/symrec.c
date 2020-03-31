#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "symrec.h"

/* Insere um símbolo na lista */
symrec *putsym (symrec *sym_table, char *sym_name, int sym_type, void *val)
{
  symrec *ptr;
  ptr = (symrec *) malloc (sizeof (symrec));

  ptr->name = (char *) malloc (strlen (sym_name) + 1);
  strcpy (ptr->name,sym_name);
  ptr->tipo = sym_type;
  ptr->value = val;
  ptr->next = (struct symrec *)sym_table;
  sym_table = ptr;
  return ptr;
}

/* Busca um símbolo */
symrec *getsym(symrec *sym_table, char *sym_name)
{
  symrec *ptr;
  for (ptr = sym_table; ptr != (symrec *) 0;
       ptr = (symrec *)ptr->next) {
    if (strcmp (ptr->name,sym_name) == 0)
      return ptr;
  }
  return 0;
}

/* Remove um símbolo */
symrec *popsym(symrec *sym_table, char *sym_name)
{
  symrec *ptr, *ant;
  if (!sym_table) return NULL;

  /* Cabeça */
  if (strcmp (sym_table->name,sym_name) == 0) {
	ptr = sym_table;
	sym_table = ptr->next;
	free(ptr);
	return sym_table;
  }

  /* Restante */
  ant = sym_table;
  for (ptr = sym_table->next; ptr != (symrec *) 0;
       ptr = (symrec *)ptr->next) {
    if (strcmp (ptr->name,sym_name) == 0) {
	  ant->next = ptr->next;
	  free(ptr);
	  return sym_table;
	}
	ant = ptr;
  }

  return sym_table;
}

/* Imprime a lista, para depuração */
void printsym(symrec *sym_table)
{
  symrec *ptr;
  for (ptr = sym_table; ptr != (symrec *) 0;
       ptr = (symrec *)ptr->next)
	printf("\t%s\n", ptr->name);  
}
