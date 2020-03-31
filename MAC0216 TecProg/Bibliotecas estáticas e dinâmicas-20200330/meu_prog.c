#include <stdio.h>

double media(double*, int);
double desvio_padrao(double*, int);

int main(){
    double vet[100];
    int i,n;

    printf("Digite a quantidade de numeros de entrada: ");
    scanf("%d", &n);

    printf("Digite %d numeros: \n", n);
    for (i=0; i < n; i++)
        scanf("%lf", &vet[i]);

    printf("media = %f \n", media(vet,n));
 
    printf("desvio padrao = %f \n", desvio_padrao(vet,n));


    return 0;
}
