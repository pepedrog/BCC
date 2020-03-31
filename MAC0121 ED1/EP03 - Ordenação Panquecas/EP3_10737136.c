#include <stdio.h>
#include <stdlib.h>

void flip(unsigned long v[], int n, int f)
{
  //Põe o primeiro no último, o penúltimo no segundo, sucessivamente
  int aux;
  for(int i = 0; i < (n - f)/2; i++)
  {
    aux = v[n - 1 - i];
    v[n - 1 - i] = v[f + i];
    v[f + i] = aux;
  } 
}

/*
void printPanquecas(unsigned long panqueca[], int n)
{
  for(int i = 0; i < n; i++) printf("%lu ", panqueca[i]);
  printf("\n");
}*/

int achaFlip(unsigned long panqueca[], int n)
{
  int menor = -1;
  int p, ult, ordenado;
  //Vamos ignorar os ultimos termos iguais, fingindo que a pilha tem um tamanho menor
  for(p = n - 2; p > 0 && panqueca[p] == panqueca[n - 1]; p--);

  //ult é o último elemento dessa pilha desconsiderando os iguais no final
  //ordenado representará quantas panquecas do final da pilha já estão ordenadas
  ult =  ordenado = p + 1;
  //Vamos analisar cada elemento da pilha
  for(p = ult - 1; p >= 0; p--)
  {
    //Se a pilha ainda está ordenada e a panqueca p é maior que anterior, então ainda está ordenado
    if(ordenado == p + 1 && panqueca[p] >= panqueca[ordenado]){
      //Se o penultimo elemento é maior que ultimo, então ele é um candidato a ser o menor
      if(p == ult - 1) menor = p;
      //Indica que esse elemento ainda está ordenado
      ordenado --;
    }
    else
      //Se a pilha não está ordenada até esse ponto, devemos achar a maior panqueca menor que a última
      //Para então flipar nessa posição para ordenar as duas
      //se menor == -1 então ainda não temos nenhum candidato a menor

      //Se a panqueca p é maior que a ultima e menor que alguma que já observamos antes, então ela é uma melhor candidata ao flip
      if(panqueca[p] >= panqueca[ult] && (menor == -1 || panqueca[p] < panqueca[menor])) menor = p;
  }
  //Se o iterador de ordenados chegou a zero, a pilha toda está ordenada
  if(ordenado == 0) return -1;
  //Se o menor termo for o penultimo, então o final da pilha já está ordenado (podendo ser os 2 ultimos ou mais)
  //Então devemos fazer um flip para colocar a base dessa sequencia ordenada no final
  if(menor == ult - 1) return ordenado;  
  //Num caso geral, encontramos a menor panqueca maior que a ultima, e vamos colocar a ultima ao lado dela
  return (menor + 1);
}

int main(void) {

  int n, maior;
  
  //Recebendo a entrada
  scanf("%d\n", &n);
  unsigned long * panquecas = malloc(n * sizeof(unsigned long));
  for(int i = 0; i < n; i++) scanf("%lu", &panquecas[i]);
  
  int nao_ordenado = 1;
  while(nao_ordenado){
    int f = achaFlip(panquecas, n);
    if(f == -1) nao_ordenado = 0;
    else {
      flip(panquecas, n , f);
      printf("%d ", f);
      //printPanquecas(panquecas, n);
    }
  }
  printf("\n");
  return 0;
}


