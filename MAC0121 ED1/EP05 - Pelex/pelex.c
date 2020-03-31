#include "../robot_fight.h"

/*Pelex o bot mais rapido do oeste

Lucas Medeiros Sobrinho 9833002
Luis Vitor Zerkowski    9837201
Pedro Gigeck Freire    10737136

*/

typedef struct ameaca{
	TileType tipo;
	int tempo;
	int dir;
	struct ameaca* prox;
} Ameaca;

typedef struct {
	Position pos;
	Direction dir;
	int dist;
} controle;

//Funcoes Auxiliares
int isControle(Grid *g, Position p) {
	return (g->map[p.x][p.y].isControlPoint);	
}

int isProjetil(Grid *g, Position p) {
    return (g->map[p.x][p.y].type == PROJECTILE);
}

int isRobo(Grid *g, Position p) {
    return (g->map[p.x][p.y].type == ROBOT);
}

int isBloco(Grid *g, Position p) {
    return (g->map[p.x][p.y].type == BLOCK);
}

int isNone(Grid* g, Position p) {
	return (g->map[p.x][p.y].type == NONE);
}

int isValid(Grid* g, Position p) {
	return (p.x >= 0 && p.x < g->m && p.y >= 0 && p.y < g->n);
}

Ameaca *mapaAmeaca[200][200];

Ameaca* novoAmeaca(){
	Ameaca* novo = malloc(sizeof(Ameaca));
	novo->prox = NULL;
	novo->tempo = 500;
	novo->dir = -1;
	novo->tipo = NONE;
	return novo;
}

void insereMapa(Position p, Ameaca* a){
	a->prox = mapaAmeaca[p.x][p.y];
	mapaAmeaca[p.x][p.y] = a;
	
}

int quickTurn(int ini, int end) {
	int i, j;
	for(i = ini, j = 0; i != end; i = (i+1)%6, j++)
		if (i >= 6) i-= 6;
	if (j > 3) j = 6-j;
	return j;
}
				
int buscaRobo(Ameaca* lista, int tempo, char controle){
	int contador = 0;
	Ameaca* aux_lista = lista;
	while(aux_lista!=NULL){
		if(aux_lista->tempo == tempo && aux_lista->tipo == ROBOT){
			if(controle == 'Q') contador++;
			else return aux_lista->dir;
		}
		aux_lista = aux_lista->prox;	
	}
	if (controle == 'Q') return contador;
	return -1;
}			   

int vasculhaPerimetro(Grid* g, int raio, Position p){
	int quant = 0;
	Position candidato = p;
	//Vasculhando os seis lados do grande hexagono que e' o perimetro
	for(int i = 0; i < 6; i++){
		candidato = p;
		//Primeiro vai em linha reta nas 6 direcoes
		for(int r = 0; r < raio; r++){
			candidato = getNeighbor(candidato, i);
		}
		
		//Depois sobe um numero de vezes pra percorrer o lado
		for(int r = 1; r < raio; r++){
			candidato = getNeighbor(candidato, (i + 2)%6);
		}
		if(isValid(g, candidato) && (isProjetil(g, candidato) || isRobo(g, candidato))) quant++;
	}
	return quant;
	
}
	
/*Dada uma direcao inicial e uma direcao final, ve
para qual lado virando eh mais rapido de se chegar*/
Action fastTurn(int ini, int end) {
	int dif = end-ini;
	if((dif <= 3 && dif >= 0) || (dif <= -3))
		return TURN_RIGHT;
	else
		return TURN_LEFT;		
}
int isControlPoint(Grid *g, Position p) {
	return (g->map[p.x][p.y].isControlPoint);	
}

int buscaProjetil(Ameaca* lista, int tempo, char retorno){
	int contador = 0;
	Ameaca* aux_lista = lista;
	while(aux_lista!=NULL){
		if(aux_lista->tempo == tempo && aux_lista->tipo == PROJECTILE){
			if(retorno == 'Q') contador++;
			else return aux_lista->dir;
		}
		aux_lista = aux_lista->prox;	
	}
	if (retorno == 'Q') return contador;
	return -1;
}

controle* controles[200];

int fimcontroles = 0;

int distanciaEfetiva(Grid* g, Direction dir, Position p, Position fim){
	if(p.x == fim.x && p.y == fim.y) return 0;
	int tamanho = g->m * g->n;
	Position atual = p, prox;
	Position fila[2*tamanho];
	int fila_dir[2*tamanho];

	int fimfila = 1;
	int inifila = 0;
	int dist_atual;
	int dir_atual;

	fila[0] = p;
	fila_dir[0] = dir;
	//Inicializando um mapa para guardar as distancias
	int mapa[g->m][g->n];
	for(int i = 0; i < g->m; i++) for(int j = 0; j < g->n; j++) mapa[i][j] = 500;

	mapa[p.x][p.y] = 0;
	//Enquanto a fila nao acaba
	while(inifila != fimfila){

		//Atualiza o atual
		atual = fila[inifila];
		dir_atual = fila_dir[inifila];
		dist_atual = mapa[atual.x][atual.y];
		inifila++;

		int quantos_adicionados = 0;
		//Vamos colocar as 6 casas vizinhas na fila
		for(int i = 0; i < 6; i++){
			//Acha a proxima posicao
			int auxi = (dir_atual + i)%6;
			prox = getNeighbor(atual, auxi);
			//puts("achei o vizinho");
			//Variavel auxiliar para ajustar a distancia das direcoes
			int auxi2;
			if(i == 5) auxi2 = 1;
			else if(i == 4) auxi2= 2;
			else auxi2 = i;

			//printf("vamos inserir na fila %d %d\n", prox.x, prox.y);
			//Se for um caminho valido, que da pra passar, que nao vai ter ameaca quando chegarmos e que ainda nao recebeu uma distancia menor que a atual
			//printf("%d\n", mapa[prox.x][prox.y], dist_atual);
			if(isValid(g, prox) && (isNone(g, prox) || isControle(g, prox)) && mapa[prox.x][prox.y] > dist_atual + auxi2 + 1){
				//puts("mesmo");
				//insere na fila
				//puts("entrei");
				fila[fimfila + quantos_adicionados] = prox;

				if(atual.x == p.x && atual.y == p.y) fila_dir[fimfila + quantos_adicionados] = auxi;
				else fila_dir[fimfila + quantos_adicionados] = dir_atual;
				//coloca no mapa
				mapa[prox.x][prox.y] = dist_atual + auxi2 + 1;

				quantos_adicionados++;
			}

		}
		fimfila += quantos_adicionados;
	}
	return mapa[fim.x][fim.y];
}

void prepareGame(Grid *g, Position p, int turnCount) {
	
	setName("Pelex");
	
	for(int i = 0; i < g->m; i++) for(int j = 0; j < g->n; j++) mapaAmeaca[i][j] = novoAmeaca();
	for(int a = 0; a < 200; a++) controles[a] = malloc(sizeof(controle));

}

Action atira(Direction from, Direction to) {
	if(to == ((from + 1) % 6))
		return SHOOT_RIGHT;
	else if(to == from)
		return SHOOT_CENTER;
	else
		return SHOOT_LEFT;
}
void atualizaControles(Grid* g, Direction direcao, Position p){
	/* Procura o ponto de controle mais rapido e verifica se nao ha nenhum robo indo naquela direcao */
	int tamanho = g->m * g->n;
	Position atual = p, prox;
	Position fila[2*tamanho];
	int fila_dir[2*tamanho];
	
	int fimfila = 1;
	int inifila = 0;
	int dist_atual;
	int dir_atual;
	
	fila[0] = p;
	fila[0] = p;
	fila_dir[0] = direcao;
	
	//Inicializando um mapa para guardar as distancias
	int mapa[g->m][g->n];
	for(int i = 0; i < g->m; i++) for(int j = 0; j < g->n; j++) mapa[i][j] = 500;
	
	mapa[p.x][p.y] = 0;
	fimcontroles = 0;
	//Enquanto a fila nao acaba
	while(inifila != fimfila){
		
		//Atualiza o atual
		atual = fila[inifila];
		dir_atual = fila_dir[inifila];
		dist_atual = mapa[atual.x][atual.y];
		inifila++;
		
		//printf("estamos olhando para %d %d inifila = %d fim fila = %d \n", atual.x, atual.y,inifila, fimfila);
		
		if(isControle(g, atual)){
			controles[fimcontroles]->pos = atual;
			controles[fimcontroles]->dir = dir_atual;
			controles[fimcontroles]->dist = dist_atual;
			fimcontroles++;
			//printf("estamos olhando para %d %d dist %d dir %d \n", atual.x, atual.y,dist_atual, dir_atual);
		}
		int quantos_adicionados = 0;
		//Vamos colocar as 6 casas vizinhas na fila
		for(int i = 0; i < 6; i++){
			//Acha a proxima posicao
			int auxi = (dir_atual + i)%6;
			prox = getNeighbor(atual, auxi);
			//puts("achei o vizinho");
			//Variavel auxiliar para ajustar a distancia das direcoes
			int auxi2;
			if(i == 5) auxi2 =1;
			else if(i == 4) auxi2 = 2;
			else auxi2 = i;
			
			//printf("vamos inserir na fila %d %d\n", prox.x, prox.y);
			//Se for um caminho valido, que da pra passar, que nao vai ter ameaca quando chegarmos e que ainda nao recebeu uma distancia menor que a atual
			//printf("%d\n", mapa[prox.x][prox.y], dist_atual);
			if(isValid(g, prox) && (isNone(g, prox) || isControle(g, prox)) && mapa[prox.x][prox.y] > dist_atual + auxi2 + 1){
				//puts("mesmo");
				//insere na fila
				//puts("entrei");
				fila[fimfila + quantos_adicionados] = prox;
				
				if(atual.x == p.x && atual.y == p.y) fila_dir[fimfila + quantos_adicionados] = (dir_atual + i)%6;
				else fila_dir[fimfila + quantos_adicionados] = dir_atual;
				//coloca no mapa
				mapa[prox.x][prox.y] = dist_atual + auxi2 + 1;
				
				quantos_adicionados++;
			}
			
		}	
		fimfila += quantos_adicionados;
	}
}

int luta(Grid *g, Robot *r, Robot *r_inimigo, controle destino) {
    if(r->bullets > 0) {
        if(destino.dir == r->dir) {
            if(r_inimigo->dir == r->dir || r_inimigo->dir == (r->dir + 1)%6 || r_inimigo->dir == (r->dir - 1)%6) {
                return 1;
            }
        }
        if(destino.dir == (r->dir + 1)%6) {
            if(r_inimigo->dir == r->dir || r_inimigo->dir == (r->dir - 1)%6) {
                return 1;
            }
        }
        if(destino.dir == (r->dir - 1)%6) {
            if(r_inimigo->dir == r->dir || r_inimigo->dir == (r->dir + 1)%6) {
                return 1;
            }
        }
        if(r->hp > r_inimigo->hp) {
            if(r->bullets*10 >= r_inimigo->hp) return 1;
            return 0;
        }
        else {
            if(r_inimigo->bullets*10 >= r->hp) return 0;
            else {
                if(r->bullets*10 >= r_inimigo->hp) return 1;
                return 0;
            }
        }
    }
	return 0;
}
int defendeProjetil(Grid *g, Position p, Robot *r, int dir_proj) {
  	//Se der pra por um obstaculo pra impedir o projetil, poe
	if(r->dir == dir_proj)
		if(isValid(g, getNeighbor(p, (r->dir + 3)%6)) && isNone(g, getNeighbor(p, (r->dir + 3)%6))) return OBSTACLE_CENTER;
    if((r->dir + 1)%6 == dir_proj)
		if(isValid(g, getNeighbor(p, (r->dir + 4)%6)) && isNone(g, getNeighbor(p, (r->dir + 4)%6))) return OBSTACLE_LEFT;
    if((r->dir - 1)%6 == dir_proj)
		if(isValid(g, getNeighbor(p, (r->dir + 2)%6)) && isNone(g, getNeighbor(p, (r->dir + 2)%6))) return OBSTACLE_RIGHT;

	//Se der pra atirar pra impedir o projetil, atira
    if(r->dir == (dir_proj + 3)%6) return SHOOT_CENTER;
    if((r->dir + 1)%6 == (dir_proj + 3)%6) return SHOOT_LEFT;
    if((r->dir - 1)%6 == (dir_proj + 3)%6) return SHOOT_RIGHT;

	return STAND;
}

				   
void atualizaMapaAmeacas(Grid* g, Position p){
	//Percorre o mapa, ao achar uma ameaca, atualiza mapaAmeaca
	Position aux, aux2, aux3;
	int contador;
	for(int i = 0; i < g->m; i++) {
        for(int j = 0; j < g->n; j++) { 
            aux.x = i;
            aux.y = j;
             //Checa se a posicao e um projetil
            if(isProjetil(g, aux)) {
                Projectile *proj = &g->map[aux.x][aux.y].object.projectile;
                Ameaca *proj_ameaca = malloc(sizeof(Ameaca));
                proj_ameaca->tipo = PROJECTILE;
                proj_ameaca->tempo = 0;
                proj_ameaca->dir = proj->dir;
                insereMapa(aux, proj_ameaca);
                contador = 1;
				aux3 = getNeighbor(aux, proj->dir);
                //Visita todas as casas no alcance e direcao do projetil e adiciona as ameaças ao mapaAmeacas
                while(isValid(g, aux3) && (isNone(g, aux3) || (aux3.x == p.x && aux3.y == p.y))){
					aux3 = getNeighbor(aux, proj->dir);
                    aux = aux3;
                    proj_ameaca = malloc(sizeof(Ameaca));
                    proj_ameaca->tipo = PROJECTILE;
                    proj_ameaca->tempo = contador;
                    proj_ameaca->dir = proj->dir;
                    insereMapa(aux, proj_ameaca);
                    contador++;
                }
            }
            //Checa se a posicao e um robo
            if(isRobo(g, aux)) {
                Robot *rob = &g->map[aux.x][aux.y].object.robot;
                Ameaca *rob_ameaca = malloc(sizeof(Ameaca));
                rob_ameaca->tipo = ROBOT;
                rob_ameaca->tempo = 0;
                rob_ameaca->dir = rob->dir;
                insereMapa(aux, rob_ameaca);
                //Visita todas as casas vazias do grid e calcula o tempo que o robo em questao demora pra alcanca-las
                for(int z = 0; z < g->m; z++) {
                    for(int w = 0; w < g->n; w++) {
                        aux2.x = z;
                        aux2.y = w;
                        if(isValid(g, aux2) && (isNone(g, aux2) || (aux2.x == p.x && aux2.y == p.y))) {
                            rob_ameaca = malloc(sizeof(Ameaca));
                            rob_ameaca->tipo = ROBOT;
                            rob_ameaca->tempo = distanciaEfetiva(g, (rob->dir)%6, aux, aux2);
                            rob_ameaca->dir = (rob->dir)%6;
                            insereMapa(aux2, rob_ameaca);
                         }                            
                     }
                 }
             }
            
        }
	}
}

int foge(Grid *g, Position p, Robot *r) {
	for(int d = 0; d < 6; d++){
		Position vizinho = getNeighbor(p, (r->dir + d)%6);
		if(isValid(g, vizinho) && isNone(g, vizinho)) {
			if(d==0) return WALK;
			return fastTurn(r->dir, (r->dir + d)%6);
		}
	}
	return STAND;
}

controle* controlePerto(Grid* g){
	controle* perto = controles[0];
	for(int i = 1; i < fimcontroles; i++)
		//Se for mais perto
		if(controles[i]->dist < perto->dist || (!isRobo(g, controles[i]->pos) && (controles[i]->dist == perto->dist))) perto = controles[i];
	
	return perto;
}
				   
int buscaControles(Position p){
	for (int i = 0; i < fimcontroles; i++) if(controles[i]->pos.x == p.x && controles[i]->pos.y == p.y) return 1;
	return 0;
}

Action processTurn(Grid *g, Position p, int turnsleft) {
    Robot *r = &g->map[p.x][p.y].object.robot;
	for(int i = 0; i < g->m; i++) for(int j = 0; j < g->n; j++){
		Ameaca* aux = mapaAmeaca[i][j];
		Ameaca* ant;
		while(aux != NULL){
			ant = aux;
			aux = aux->prox;
			free(ant);
		}
	}
	for(int i = 0; i < g->m; i++) for(int j = 0; j < g->n; j++) mapaAmeaca[i][j] = novoAmeaca();
	atualizaMapaAmeacas(g, p);
	
	atualizaControles(g, r->dir, p);
    //Se estamos num control point
	if(buscaControles(p)){ 
		//Vamos nos protejer!
		//Caso dos vizinhos (raio 1)
		int num_ameacas = vasculhaPerimetro(g, 1, p);
		//So vamos tratar se nao sobrevivermos
		if(r->hp < num_ameacas*10) return foge(g, p, r);
		//Caso raio 2;
		
		else if(buscaRobo(mapaAmeaca[p.x][p.y], 2, 'Q') + buscaProjetil(mapaAmeaca[p.x][p.y], 2, 'Q') > 0){
			int dir_proj = buscaProjetil(mapaAmeaca[p.x][p.y], 2, 'D');
			int dir_robo = buscaRobo(mapaAmeaca[p.x][p.y], 2, 'D');
			if(r->bullets == 0 || r->obstacles == 0) return STAND;
			if(dir_robo >= 0) return defendeProjetil(g, p, r, dir_robo);
			else defendeProjetil(g, p, r, dir_proj);
		}
		else return STAND;
	}
	//Se nao estamos num ponto de controle
	else{
		controle *destino;
		//Acha o ponto de controle livre mais proximo, considerando as ameacas do caminho
		destino = (controlePerto(g));
		//Se tem um robo no destino escolhido, entao todos os controles tem robo
		if(isRobo(g, destino->pos)){
			//Se estamos perto, vira pra direcao e atira
			if(destino->dist < 2){
                if(luta(g, r, &g->map[destino->pos.x][destino->pos.y].object.robot, *destino)) {
                    if(destino->dir == r->dir) return SHOOT_CENTER;
                    if(destino->dir == (r->dir + 1)%6) return SHOOT_LEFT;
                    if(destino->dir == (r->dir - 1)%6) return SHOOT_RIGHT;
                    else return fastTurn(r->dir, destino->dir);
                }
                destino->dist = 500;
                destino = (controlePerto(g));
			}
		}
		//printf("Vamos para %d %d com distancia %d na direcao %d\n", destino->pos.x, destino->pos.y, destino->dist, destino->dir);
		//Retorna a acao pra chegar ao destino
		if(destino->dir == r->dir) return WALK;
		else return fastTurn(r->dir, destino->dir);
	}
	
	return STAND;
}


