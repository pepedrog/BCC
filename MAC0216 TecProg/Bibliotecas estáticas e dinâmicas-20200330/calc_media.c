double media(double* vet, int n){
    int i;
    double soma = 0;

    for (i=0; i < n; i++)
        soma += vet[i];

    return soma/n;
}
