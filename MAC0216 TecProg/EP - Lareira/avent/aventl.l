%{
#include "symrec.h"
#include "avent.tab.h"

/* Para readline */
#include <readline/readline.h>
#include <readline/history.h>

/* Redefinição da entrada do Flex para usar o readline */
#define YY_INPUT(buf,result,max_size) result = mygetinput(buf, max_size);


/* Função que substitui a entrada */
static int mygetinput(char *buf, int size) {
  char *line;
  /* final de arquivo */
  if (feof(yyin))  return YY_NULL;

  /* Lê uma linha, com o prompt "> " */
  line = readline("> ");
  if(!line)        return YY_NULL;

  /* segurança */
  if(strlen(line) > size-2){
     fprintf(stderr,"input line too long\n");
	 return YY_NULL;
  }

  /* copia para o buffer de enrtada */
  sprintf(buf,"%s\n",line);
  /* adiciona ao histórico */
  add_history(line);

  /* libera memória */
  free(line);
  return strlen(buf);
}   
%}

/* Não importa se maiúsculas ou minúsculas */
%option caseless


/* em unicode, á são dois caracteres, veja as regras para INVENT e VAPARA */

%%

(fim|Chega) { return FIM;}

<<EOF>> { puts("Bye bye..."); return FIM; }


i(nvent((a|á|Á)rio)?)?  { return INVENT;}

v(á|Á|a)[[:space:]]+para {
  return VAPARA;}

(N|Norte|NORTE) { return NORTE;}
(S|Sul|SUL)     { return SUL;}
(L|Leste|LESTE) { return LESTE;}
(W|Oeste|OESTE) { return OESTE; /* W no lugar de O para evitar confusão com o artigo 'o'*/  } 
(C|Cima|CIMA)   { return CIMA;}
(B|Baixo|BAIXO) { return BAIXO;}


[ao]|uma?

d[aoe]|em|n[ao]

[[:alpha:]]+ {
			   /* identificador */
               symrec *s;
			   if ((s = getsym(sym_table, yytext))) {
				 yylval.tptr = s;
				 return s->tipo;
			   }
			   else {
				 yylval.str = yytext;
				 return DESC;
			   }
			  }


[ \t]+
[\n;] {/* ';' também termina linhas */return EOL;}


. {yylval.str = yytext; return DESC;}
