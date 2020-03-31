typedef enum {
  OPERADOR, 
  NUMERO, 
  VARIAVEL, 
  INVALIDO, 
  PAR_ESQ, 
  PAR_DIR,
  COL_ESQ, 
  COL_DIR, 
  ATRIBUI, 
  SENO,
  COSSENO,
  RAIZ,
  FIM, 
  PRINT
} TOKEN;

TOKEN analex();

/* Variaveis globais */

extern double num;
extern TOKEN ilc;
extern char ch;






