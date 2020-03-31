#include <stdio.h>
#include "recur.h"

int main()
{
  analex();
  do {
    printf(">%10.3f\n", expr());
    if (ilc == PRINT) analex();
  } while (ilc != FIM);
  return 0;
}


