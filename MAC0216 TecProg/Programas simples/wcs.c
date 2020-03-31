#include <stdio.h>

typedef enum { NO, YES } BOOLEAN;

unsigned long int numwords(char *s)
{
    unsigned long int nw;
    int c;
    BOOLEAN inword;

    inword = NO;
    nw = 0;

    while (c = *s++) {
	  if (c == ' ' || c == '\n' || c == '\t')
		inword = NO;
	  else if (inword == NO) {
		puts(s);
		inword = YES;
		++nw;
	  }
    }

    return nw;
}

int main()
{
  char *m = "String  de teste com \n newlines dentro\n";
  printf("%lu\n", numwords(m));
  return 0;
}
