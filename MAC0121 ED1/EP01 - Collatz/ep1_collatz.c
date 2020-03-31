#include <stdio.h>
#include <stdlib.h>
 
typedef struct{
  int numero;
  int passos;
}passos;

typedef passos * Passos;

//Função que não está funcionando para realocar o tamanho do vetor de passso :[ 
void resize(Passos * v, int * max){
  Passos * novo;
  *max = 2*(*max);
  novo = malloc((*max)*sizeof(passos));
  for(int i = 0; i<(*max - 1); i++) novo[i] = v[i];
  free(v);
  v = malloc((*max) * sizeof(passos));
  v = novo;
}

//Função para adicionar um novo passo ao vetor de passos conhecidos
void addPassos(Passos * v, int * topo, int * max, Passos p){
  if(*topo >= *max - 1) resize(v,max);
  int i = *topo/2;
  int ini = 0;
  int fim = *topo;
  
  //Faz uma busca pra descobrir onde inserir o p
  while(i != *topo && (v[i]->numero > p->numero || v[i+1]->numero < p->numero)){
   if(v[i]->numero > p->numero){ 
     fim = i;
     i = (ini+1)/2; ;
     
   }
   else{
     ini = i;
     i = (i + fim + 1)/2;
   } 
  }
  
  i++;
  
  //passa todos para direita e adiciona o novo elemento no lugar determinado ii
  int ii = i;
  Passos auxx = v[i];
  Passos aux;
  for (i; i<=(*topo); i++){
     if (i != *topo) aux = v[i + 1];
     v[i + 1] = auxx;
     if (i != *topo)auxx = aux;
  }
  v[ii] = p;
  *topo = *topo + 1;
}

//Função que busca um número na lista de passos
int buscaPassos(Passos * v, int topo, int procurado){
  //Se ele é menor que o primeiro ou maior que o último, ou se a lista está vazia
  if (v[topo]->numero < procurado) return(-1);
  int ini = 0;
  int fim = topo;
  //Vai procurar com uma tentativa de busca binC!ria
  int i = topo/2;
  while(v[i]->numero != procurado){
    if(v[i]->numero > procurado){ 
      if(v[i - 1]->numero >= procurado){
          fim = i;
          i = ini/2;
      }
      else return(-1);
    }
    else if(v[i + 1]->numero <= procurado){
        ini = i;
        i = (i + fim + 1)/2;
    }
    else return(-1);
  }
  //retorna os passos do elemento encontrado, ou então -1 se não encontrar
  return(v[i]->passos);
}

//Collatz Padrão
int collatz(int n){
  if(n%2 == 1) return(3*n + 1);
  else return(n/2);
}

//Função para calcular os passos
int passosCollatz(Passos * passos_conhecidos, int * topo, int * max, int n){
  //Se já calculei os passos para esse número, estão armazenados e  sei buscá-los
  int p;
  p = buscaPassos(passos_conhecidos, *topo, n);
  //Se encontrei p, retornar p
  if(p > 0) return p;

  //Se ainda não conheçe os passos:

  //Vetor para guardar o caminho e o índice dele, que será o número de passos
  int * n_aux = malloc(200*sizeof(int));
  int i = 1;

  //O primeiro item é o próprio n
  n_aux[0] = n;
 
  //Enquanto não encontrar um n que já conheço os passos
  while(p < 0){
    //Aplica a funC'C#o
    n_aux[i] = collatz(n_aux[i - 1]);
    //Verifica se jC! conheC'o o novo n
    p = buscaPassos(passos_conhecidos, *topo, n_aux[i]);
    //Incrementa os passos
    i++;
  }
  i = i - 2;
  //Guardo quanto passos dei atC) chegar em um conhecido
  int mod_i = i;

  //Adiciono todos esses novos passos no vetor de passos_conhecidos
  for(i; i>=0; i--){
    Passos novo;
    novo = malloc(sizeof(passos));
    novo->numero = n_aux[i];
    novo->passos = p + mod_i - i + 1;

    addPassos(passos_conhecidos, topo, max, novo);

  }
  free(n_aux);
  //retorna os passos do conhecido + os passos dados pra chegar nele
  return(p + mod_i + 1);
}

int main(void) {
  int i, f, n;
  scanf("%d%d", &i, &f);
  Passos * passos_conhecidos;

  int * topo;
  topo = malloc(sizeof(int));
  *topo = 0;
  int * max;
  max = malloc(sizeof(int));
  *max = 100000;
  passos_conhecidos = malloc((*max)*sizeof(passos));

  Passos primeiro;
  primeiro = malloc(sizeof(passos));
  primeiro->numero = 1;
  primeiro->passos = 0;
  passos_conhecidos[0] = primeiro;

  for(n = i; n <= f; n++){
    //print um pouco mais didático
    //printf("%d:%d:%d\n", n, passosCollatz(passos_conhecidos, topo, max, n),*topo);
    printf("%d\n",passosCollatz(passos_conhecidos, topo, max, n));
  }
}