		unsigned long int nl = 0, np = 0, nc = 0;
PALAVRA [[:alnum:]ã_]+

%%
\n	++nc;++nl;

{PALAVRA}  {
				++np; nc+=yyleng;
				printf("Palavra reconhecida %s\n", yytext);
		   }

.	++nc;

%%

int main() {
	yylex();
	printf("%lu %lu %lu \n", nc, np, nl);
	return 0;
}

