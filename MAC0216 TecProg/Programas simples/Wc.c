#include <stdio.h>

typedef enum { NO, YES } BOOLEAN;

int main()
{
    unsigned long int nl, nw, nc;
    int c;
    BOOLEAN inword;

    inword = NO;
    nl = nw = nc = 0;
    while ((c = getchar()) != EOF) {
        ++nc;
		if (c == '\n') ++nl;
		if (c == ' ' || c == '\n' || c == '\t')
		  inword = NO;
		else if (inword == NO) {
		  inword = YES;
		  ++nw;
		}
    }
    printf ("%lu %lu %lu\n", nl, nw, nc);
    return 0;
}

