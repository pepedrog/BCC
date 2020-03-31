/* -*- mode:c -*- */
/* leitor de arquivos .ini do Windows */

NOME	 [[:upper:][:lower:][:digit:]. ]+
ENTRADA  [*]?[A-Za-z0-9. ]+
SEP		 [[:space:]]*

		 int achou=1;			/* gambiarra */

%x VALOR

%%

^\[{NOME}\] {
				  if (!achou) {
					puts("VAZIA\n");
				  }
				  yytext[yyleng-1] = '\0';
				  puts("------------------------------");
				  printf("Seção: %s\n", ++yytext);
				  puts("------------------------------");
				  achou=0;
			   }

^{ENTRADA}	   {
			     printf("%-20.20s", yytext);
				 BEGIN(VALOR);
			   }

<VALOR>={SEP}$ {
					printf("=> não tem valor associado");
					BEGIN(0);
				 }


<VALOR>=[^[:space:]]+.*$ {
				  printf("-> %s", ++yytext);
				  achou =1;
				  BEGIN(0);
			   }

<VALOR>.+ {
				  printf("Algo estranho: %s\n", yytext);
				  BEGIN(0);
			}

^{SEP}+$



