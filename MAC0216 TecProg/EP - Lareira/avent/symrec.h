struct symrec
{
  char *name;					/* nome           */
  int tipo;						/* tipo			  */
  void *value;					/* Valor genérico */
  struct symrec *next;			/* próximo        */
};

typedef struct symrec symrec;

/* The symbol table: a chain of `struct symrec'.     */
extern symrec *sym_table;

symrec *putsym(symrec*, char *, int, void *);
symrec *getsym(symrec*, char *);
symrec *popsym(symrec *, char *);

void printsym(symrec *);


