#include <stdio.h>
int main(){

	int n;
	int p = 0;
	scanf("%d", &n);
	int ant1[2], ant2[2], atual[2];
	scanf("%d %d", &ant2[0], &ant2[1]);
	scanf("%d %d", &ant1[0], &ant1[1]);
	if(ant1[0] == ant2[0])
		for(int i = 0; i < n; i++){
			scanf("%d %d", &atual[0], &atual[1]);
			//se vim de baixo e virei a esquerda
			if((ant2[1] < ant1[1] && ant1[0] > atual[0]) || (ant2[1] > ant1[1] && ant1[0] < atual[0]) || (ant2[0] < ant1[0] && ant1[1] < atual[1]) || (ant2[0] > ant1[0] && ant1[1] > atual[1]))
			{
				p++;
			}
			
			ant2[0] = ant1[0];
			ant2[1] = ant1[1];
			ant1[0] = atual[0];
			ant1[1] = atual[1];
		}
	else
		for(int i = 0; i < n; i++){
			scanf("%d %d", &atual[0], &atual[1]);
			//se vim de baixo e virei a esquerda
			if(ant2[0] == ant1[0])
			if(!((ant2[1] < ant1[1] && ant1[0] > atual[0]) || (ant2[1] > ant1[1] && ant1[0] < atual[0]) || (ant2[0] < ant1[0] && ant1[1] < atual[1]) || (ant2[0] > ant1[0] && ant1[1] > atual[1])))
				p++;
			
			ant2[0] = ant1[0];
			ant2[1] = ant1[1];
			ant1[0] = atual[0];
			ant1[1] = atual[1];
			
		}
	
	printf("%d\n", p);
	return 0;
}