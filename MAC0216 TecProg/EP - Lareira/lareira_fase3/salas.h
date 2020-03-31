#include "hash.h"
typedef int (*fptr)(Elemento*, Elemento*);

Elemento* atual;
Elemento sala1, sala2, sala3, sala4, sala5, sala6, personagem, mascara, pessoas;
Elemento quadro, gramo, disco, balao, arma, cogumelos, homem, garrafa, espelho, cama, envelope, carta, foto;
Lista* sym_table;
void salas(void);