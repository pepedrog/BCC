#include "stdio.h"
int main(){
	
	int n;
	scanf("%d", &n);
	int v[4];
	for(int i = 0; i < n; i++){
		scanf("%d %d %d %d", &v[0], &v[1], &v[2], &v[3]);
		if(v[0] != v[2]) printf("%d %d", v[0], v[2]);
		else printf("%d %d", v[0], v[3]);
		printf("\n");
	}
	return 0;
}