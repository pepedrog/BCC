#include <stdio.h>
#include <stdlib.h>

/* --------------------------------------
                   PILHA 
         (implementação das aulas)
   -------------------------------------- */


typedef int Tipo;

typedef struct{
  Tipo * v; 
  int topo;
  int max;
} pilha;

typedef pilha * Pilha;

Pilha CriaPilha(int max){
  Pilha P = malloc(sizeof(pilha));
  P->v = malloc(max*sizeof(pilha));
  P->topo = 0;
  P->max = max;
  return P;
}

int PilhaVazia(Pilha P){
  if(P->topo == 0) return 1;
  return 0;
}

void DestroiPilha(Pilha P){
  free(P->v);
  free(P);
}

void resize(Pilha P){
  Tipo * novo = malloc(2*P->max*sizeof(Tipo));
  for(int i = 0; i < P->max; i++) 
    novo[i] = P->v[i];
  free(P->v); 
  P->v = novo;
  P->max = P->max *2;
}

void Empilha(Pilha P, Tipo obj){
  if(P->topo == P->max) resize(P);
  P->v[P->topo] = obj;
  P->topo++;
}

void Desempilha(Pilha P){
  if(PilhaVazia(P)) printf("Erro!");
  else P->topo--;
}

Tipo TopoDaPilha(Pilha P){
  if(PilhaVazia(P)){
    printf("ERRO!\n");
    return '0';
  }
  return (P->v[P->topo - 1]);
}

/* --------------------------------------
               FIM DE PILHAS
   -------------------------------------- */

/* --------------------------------------
            FUNÇÕES AUXILIARES
   -------------------------------------- */

//mede tamanho da string
int strlen(char* s)
{
  int i;
  for(i = 0; s[i] != '\0'; i++);
  return i;
}

//tenta colocar uma letra em uma posição
int tentaColocar(char ** tab[], int m, int n, int i, int j, char letra)
{
  //se não está fora do tabuleiro, e é uma posição colocável, coloca
  if(i < m && j < n && (tab[i][j][0] == '0' || tab[i][j][0] == letra))
  {
    if(tab[i][j][0] == '0') tab[i][j][0] = letra;
    else tab[i][j][1] = letra;
    return 1;
  }
  return 0; 
}

//tenta preencher uma palavra, começando em alguma posição com alguma orientação (indicadas por tent)
int tentaPreencher(char ** tab[], int m, int n, char palavra[], int tent)
{
  /*
      tent é um número entre 0 e 2*m*n
      tent(i, j, ori) = j*m + j*2 + ori

      ** Se tent for par, a tentativa deve preencher a palavra de pé, se ímpar, deitada
      ** (tent / 2) % m representa a coluna
      ** tent / 2m representa a linha
      
      Assim, ao invés de guardar um vetor com linha, coluna e orientação, 
      podemos só guardar um número
      
      Exemplo m = n = 3
      linha  coluna  ori - tent
        0      0      0      0
        0      0      1      1
        0      1      0      2
        0      1      1      3
        0      2      0      4
        0      2      1      5
        1      0      0      6
        1      0      1      7
        1      1      0      8
        1      1      1      9
                 assim vai
  */
  int ori = tent%2;
  int i = tent/2 % m;
  int j = tent / (2*m);

  int tam = strlen(palavra);

  int l; //indice pra percorrer a palavra
  if(ori)
  {
    //se a orientação for horizontal

    //se o tamanho da palavra for maior que o pedaço de linha
    //ou ela não começar em uma borda (começar no meio da linha), não poderá ser preenchida
    if(tam > n - j || (j > 0 && tab[i][j-1][0] != '-')) return 0;

    //Enquanto a palavra não acabar e não acabar o espaço e 
    //aonde queremos preencher for 0 ou letra que queremos por
    for(l = 0; l < tam && tentaColocar(tab, m, n, i, j, palavra[l]); l++, j++);
    //se chegou no final da palavra e chegou em alguma borda (palavra maximal), deu certo
    if(l == tam && (j == n || tab[i][j][0] == '-')) return 1;
    l--;
    //se não deu certo, tem que retirar o que colocou
    for(l; l > -1; l--) 
    {
      j--;
      if(tab[i][j][1] != '0') tab[i][j][1] = '0';
      else tab[i][j][0] = '0';
    }
    return 0;
  }
  else
  {
    //se a orientação for vertical, mesma coisa
    if(tam > m - i || (i > 0 && tab[i-1][j][0] != '-')) return 0;
    for(l = 0; l < tam && tentaColocar(tab, m, n, i, j, palavra[l]); l++, i++); 
    if(l == tam && (i == m || tab[i][j][0] == '-')) return 1;
    l--;
    for(l; l > -1; l--) 
    {
      i--;
      
      if(tab[i][j][1] != '0') tab[i][j][1] = '0';
      else tab[i][j][0] = '0';
      
    }
    return 0;
  }
}

void despreenche(char ** tab[], int m, int n, int tent)
{
  //Bastante parecido com tenta preencher
  int ori = tent%2;
  int i = (tent/2) % m;
  int j = tent / (2*m);
  if(ori)
  {
    //Enquanto não chegar em alguma parede
    for(j; j < n && tab[i][j][0] != '-'; j++)
      //Se o último ta preenchido, despreenche ele
      if(tab[i][j][1] != '0') tab[i][j][1] = '0';
      //Se não, despreenche o primeiro
      else tab[i][j][0] = '0';
  }
  else
  {
    //mesma coisa para outra orientação
    for(i; i < m && tab[i][j][0] != '-'; i++)
      if(tab[i][j][1] != '0') tab[i][j][1] = '0';
      else tab[i][j][0] = '0';
  } 

  // O intuito de fazer com char[2] é que ao apagar uma palavra, não apaga parte da outra
  // Se tem uma palavra preenchida na vertical e uma na horizontal, a posicao da interseção
  // ficaria algo como tab[i][j] = {a, a}
  
  // Dai quando despreencher uma delas, não apagaremos a letra a da outra!
}

//Imprime na saída padrão da palavra cruzada
void printTab(char** tab[], int m, int n)
{
  for(int i = 0; i < m; i++)
  {
    for(int j = 0; j < n; j++)
    {
      if(tab[i][j][0] == '-') printf(" *");
      else printf(" %c",tab[i][j][0]);   
    }
    printf("\n");
  }
}

/* --------------------------------------
           FIM FUNÇÕES AUXILIARES
   -------------------------------------- */


/* --------------------------------------

           FUNÇÃO PRINCIPAL DO EP
                
   -------------------------------------- */

int palavraCruzada(char ** tabuleiro[], int m, int n, char* palavras[], int pa)
{
  
  Pilha pilha = CriaPilha(pa);
  int p = 0; //índice das palavras
  int desempilhou = 0; //flags 
  int tent; //número que indica de forma unívoca uma posição e orientação 
            //Funcionamento explicado na função tentaPreencher

  //Vamos tentar empilhar cada palavra
  while(p < pa)
  {
    //Se não veio de uma desempilhada, podemos testar todas as possibilidades
    if(!desempilhou) tent = 0;

    for(tent; tent < 2*m*n && !tentaPreencher(tabuleiro, m, n, palavras[p], tent); tent++);

    if(tent < 2*m*n)     
    {
      Empilha(pilha, tent);
      p++;
      desempilhou = 0;
    }
    else 
    {
      //backtrack
      if(PilhaVazia(pilha)) return 0;
      desempilhou = 1;
      tent = TopoDaPilha(pilha); //Vamos despreencher a ultima palavra que preenchemos  
      despreenche(tabuleiro, m, n, tent);
      tent++; //da onde iremos começar a tentar (pra nao fazer repetidas)
      Desempilha(pilha);
      p--;
    }   
  }
  return 1;
}

int main(void)
{
  //variáveis da especificação em vetores[2] (uma para cada instancia)
  int m[2], n[2], p[2];
  char** palavras[2];
  int** tab[2];
  int i; //indice de vários for

  //Iteração pras entradas
  for(int instancia = 1; instancia < 3; instancia++)
  {
    scanf("%d %d", &m[instancia], &n[instancia]);

    tab[instancia] = malloc(m[instancia]*sizeof(int*));

    for(i = 0; i < m[instancia]; i++) tab[instancia][i] = malloc(n[instancia]*sizeof(int));
  
    for(i = 0; i < m[instancia]; i ++)
    {
      for(int j = 0; j < n[instancia]; j++) scanf("%d", &tab[instancia][i][j]);
    }

    scanf("%d", &p[instancia]);
  
    palavras[instancia] = malloc(p[instancia]*sizeof(char*));
    for(i = 0; i < p[instancia]; i++) palavras[instancia][i] = malloc((m[instancia] + n[instancia])*sizeof(char));

    for(i = 0; i < p[instancia]; i++) scanf("%s", palavras[instancia][i]);

  }
  //Confirmação que acabou a entrada (0 0)
  int c,d;
  scanf("%d %d", &c, &d);
  if(c != 0 || d != 0) 
  {
    printf("Erro na entrada!\n");
    return 1;
  }
  
  //Iteração pra saída e processamento
  for(int inst = 1; inst < 3; inst++)
  {
    //transformando o tab em uma matriz de char[2], que foi como o algoritmo foi implementado (explicado na função despreenche)
    char*** tab_c;
    tab_c = malloc(m[inst]*sizeof(char**));
    for(i = 0; i < m[inst]; i++) tab_c[i] = malloc(n[inst]*sizeof(char*)); 
    for(i = 0; i < m[inst]; i++) 
    {
      for(int j = 0; j < n[inst]; j++)
      {
        tab_c[i][j] = malloc(2*sizeof(char));
        if(tab[inst][i][j] == -1)
        {
          tab_c[i][j][0] = '-';
          tab_c[i][j][1] = '1';
        }
        else
        {
          tab_c[i][j][0] = '0';
          tab_c[i][j][1] = '0';        
        }
      }  
      free(tab[inst][i]);
    }  
    free(tab[inst]);

    //Chamando e já imprimindo a função que basicamente realizará todo o trabalho
    printf("\nInstancia %d\n", inst);
    if(palavraCruzada(tab_c, m[inst], n[inst], palavras[inst], p[inst])) printTab(tab_c, m[inst], n[inst]);
    else printf("nao ha solucao\n");
    for(i = 0; i < p[inst]; i++) free(palavras[inst][i]);
    
    //terminando de liberar os ponterios
    free(palavras[inst]);
    for(i = 0; i < m[inst]; i++) free(tab_c[i]);

    free(tab_c);
  
  }  
  return 0;
}

// -----------------------------------------------------   :D


