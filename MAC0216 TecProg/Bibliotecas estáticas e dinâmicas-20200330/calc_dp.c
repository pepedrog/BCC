#include <math.h>

double desvio_padrao(double* vet, int n){
    int i;
    double media = 0, dp = 0;

    for (i=0; i < n; i++)
        media += vet[i];

    media /= n;
    for (i=0; i < n; i++)
        dp += pow((media-vet[i]),2);

    return sqrt(dp);
}
