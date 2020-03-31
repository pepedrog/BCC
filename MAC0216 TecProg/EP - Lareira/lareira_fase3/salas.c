#include "hash.h"
typedef int (*fptr)(Elemento*, Elemento*);

Elemento* atual;
Elemento sala1, sala2, sala3, sala4, sala5, sala6, personagem, mascara, pessoas;
Elemento quadro, gramo, disco, balao, arma, cogumelos, homem, garrafa, espelho, cama, envelope, carta, foto;

void salas(){
	personagem.nome = "você";
	personagem.longa = "Esse é você mesmo. Não tem muito que você se lembre sobre.";
	personagem.curta = "Você mesmo.";
	personagem.ativo = True;
	personagem.visivel = True;
	personagem.conhecido = False;
	personagem.conteudo = Tcria(4);

	quadro.nome = "quadro";
	quadro.artigos = malloc(2*sizeof(string));
	quadro.artigos[0] = "o";
	quadro.artigos[1] = "um";
	quadro.longa = "Um quadro escrito ALGUMA COISA ESCAPA AO NAUFRÁGIO DAS ILUSÕES";
	quadro.curta = "um quadro";
	quadro.ativo = True;
	quadro.visivel = True;
	quadro.conhecido = False;
	quadro.conteudo = Tcria(4); //o quadro não contém nada


	sala1.nome = "sala inicio";
	sala1.artigos = malloc(2*sizeof(string));
	sala1.artigos[0] = "a";
	sala1.artigos[1] = "uma";
	sala1.longa = "BEM-VINDO AO INICIO.\n"
	"É uma sala claustrofóbica e pouco iluminada.\n"
	"Tudo o que existem são quatro portas ao seu redor, uma em cada parede.\n"
	"Em uma das paredes há também um grande quadro com algo escrito.";
	sala1.curta = "Esta é a sala inicial, aquela na qual você acordou.";
	sala1.ativo = True;
	sala1.visivel = True;
	sala1.conhecido = True;
	sala1.conteudo = Tcria(4);
	//sala1.def.lugar.saidas = malloc(4*sizeof(Elemento*));
	sala1.def.lugar.saidas[0] = &sala4;
	sala1.def.lugar.saidas[1] = &sala4;
	sala1.def.lugar.saidas[2] = &sala2;
	sala1.def.lugar.saidas[3] = &sala3;
	Tinsere((sala1.conteudo), &quadro);

	atual = &sala1;

	disco.nome = "disco";
	disco.artigos = malloc(2*sizeof(string));
	disco.artigos[0] = "o";
	disco.artigos[1] = "um";
	disco.longa = "Um disco de vinil sem informações, encontrado no gramofone e sem capa por perto.";
	disco.curta = "O disco de vinil.";
	disco.ativo = False;
	disco.visivel = False;
	disco.conhecido = False;
	disco.conteudo = Tcria(4);


	gramo.nome = "gramofone";
	gramo.artigos = malloc(2*sizeof(string));
	gramo.artigos[0] = "o";
	gramo.artigos[1] = "um";
	gramo.longa = "Um gramofone autêntico, antigo mas muito bem conservado.\n"
	"Sua caixa é feita de madeira envernizada e o amplificador é dourado, muito delicado.\n"
	"Nele há um disco de vinil";
	gramo.curta = "O autêntico gramofone.";
	gramo.ativo = False;
	gramo.visivel = False;
	gramo.conhecido = False;
	gramo.conteudo = Tcria(4);
	Tinsere((gramo.conteudo), &disco);


	balao.nome = "balão";
	balao.artigos = malloc(2*sizeof(string));
	balao.artigos[0] = "o";
	balao.artigos[1] = "um";
	balao.longa = "Um balão vermelho, cheio de ar";
	balao.curta = "O balão vermelho.";
	balao.ativo = False;
	balao.visivel = False;
	balao.conhecido = False;
	balao.conteudo = Tcria(4);

	//Elemento sala2;
	sala2.nome = "audicao";
	sala2.artigos = malloc(2*sizeof(string));
	sala2.artigos[0] = "a";
	sala2.artigos[1] = "uma";
	sala2.longa = "BEM-VINDO À AUDIÇÃO.\n"
	"Nessa sala toca uma música melodiosa, muito agradável.\n"
	"A melodia penetra seus ouvidos e eleva os humores, lhe causando uma sensação de pertencimento.\n"
	"Há aqui um gramofone (a música parece vir de lá) e um balão.";
	sala2.curta = "Esta é a sala onde toca uma música.";
	sala2.ativo = True;
	sala2.visivel = True;
	sala2.conhecido = False;
	sala2.conteudo = Tcria(4);
	Tinsere((sala2.conteudo), &gramo);
	Tinsere((sala2.conteudo), &balao);
	sala2.def.lugar.saidas[0] = &sala5;
	sala2.def.lugar.saidas[1] = &sala5;
	sala2.def.lugar.saidas[2] = &sala3;
	sala2.def.lugar.saidas[3] = &sala1;


	//Elemento personagem;
	//Sala 3

	//Iniciando os atributos
	sala3.nome = "sala sociedade";
	sala3.artigos = malloc(2*sizeof(string));
	sala3.artigos[0] = "a";
	sala3.artigos[1] = "uma";
	sala3.longa = "BEM-VINDO À SOCIEDADE.\n"
	"Uma mascara chama bastante atencao no canto da sala,\n"
	"Do outro lado, um grupo de pessoas parece se divertir..";
	sala3.curta = "Sala sociedade.";
	sala3.ativo = True;
	sala3.visivel = True;
	sala3.conhecido = False;
	sala3.def.lugar.saidas[0] = &sala6;
	sala3.def.lugar.saidas[1] = &sala6;
	sala3.def.lugar.saidas[2] = &sala1;
	sala3.def.lugar.saidas[3] = &sala2;

	//Criando os elementos da sala;
	//Mascara
	mascara.nome = "mascara";

	mascara.artigos = malloc(2*sizeof(string));
	mascara.artigos[0] = "a";
	mascara.artigos[1] = "uma";

	mascara.longa = "Uma mascara bem chamativa, nao parece muito com voce\n"
					"Mas de alguma maneira voce parece gostar mais da mascara que de si proprio.";
	mascara.curta = "Uma mascara muito atraente";
	mascara.ativo = False;
	mascara.visivel = False;
	mascara.conhecido = False;

	mascara.def.objeto.lista = malloc(3*sizeof(atrib));
	mascara.def.objeto.lista[0].quali = "social"; //mascara social
	mascara.def.objeto.lista[1].quali = "atraente";
	mascara.def.objeto.lista[2].quali = "chamativa";

	//Grupo de pessoas
	pessoas.nome = "grupo de pessoas";
	pessoas.longa = "Um grupo bem animado de pessoas, parecem estar se divertindo bastante";
	pessoas.curta = "Grupinho de pessoas";
	pessoas.ativo = True;
	pessoas.visivel = True;
	pessoas.conhecido = False;
	pessoas.artigos = malloc(2*sizeof(string));
	pessoas.artigos[0] = "o";
	pessoas.artigos[1] = "um";

	sala3.conteudo = Tcria(4);
	Tinsere((sala3.conteudo), &mascara);
	Tinsere((sala3.conteudo), &pessoas);


	sala4.nome = "Remanescencia";
	sala4.artigos = malloc(2*sizeof(string));
	sala4.artigos[0] = "a";
	sala4.artigos[1] = "uma";
	sala4.longa = "BEM-VINDO À REMANESCÊNCIA.\n"
				  "Uma mistura nostalgica de companheirismo e solidao\n"
		          "Toma conta do seu coracao quando nessa sala\n"
				  "Nela, voce encontra cartas e uma envelope.";
	sala4.curta = "Sala remanescencia, com as cartas e um envelope.";
	sala4.ativo = False;
	sala4.visivel = True;
	sala4.conhecido = False;


	//Definindo as saidas
	sala4.def.lugar.saidas[0] = &sala1;
	sala4.def.lugar.saidas[1] = &sala1;
	sala4.def.lugar.saidas[2] = &sala5;
	sala4.def.lugar.saidas[3] = &sala6;


	//Definindo os elementos
	foto.nome = "fotografia";

	foto.artigos = malloc(2*sizeof(string));
	foto.artigos[0] = "a";
	foto.artigos[1] = "uma";

	foto.longa = "Uma linda foto de um casal em um parque,\n"
				 "Estao assistindo a um por do sol, abracados\n"
				 "Um registro de um momento perfeito, eterno..";
	foto.curta = "Foto romantica de um casal";
	foto.ativo = False;
	foto.visivel = False;
	foto.conhecido = False;

	foto.def.objeto.lista = malloc(sizeof(atrib));
	foto.def.objeto.lista[0].quali = "romantica";

	envelope.nome = "envelope";

	envelope.artigos = malloc(2*sizeof(string));
	envelope.artigos[0] = "o";
	envelope.artigos[1] = "um";

	envelope.longa = "Um envelope sem destinatario, parece haver uma carta dentro.";
	envelope.curta = "Envelope em branco";
	envelope.ativo = False;
	envelope.visivel = False;
	envelope.conhecido = False;

	carta.nome = "carta";

	carta.artigos = malloc(2*sizeof(string));
	carta.artigos[0] = "a";
	carta.artigos[1] = "uma";

	carta.longa = "Uma carta manuscrita com um poema romantico,\n"
				  "Ao longo do papel, manchas de lagrimas ja secas\n"
				  "Voce reconhece a caligrafia... mas nao consegue se lembrar da onde\n"
				  "O texto lhe traz uma saudade incompreensivel, e ao mesmo tempo um acolhimento amoroso\n"
				  "Quanto mais se le, mais dor, quanto mais dor, mais vontade de ficar na companhia daquelas palavras.";
	carta.curta = "carta amorososa";
	carta.ativo = False;
	carta.visivel = False;
	carta.conhecido = False;

	
	
	sala4.conteudo = Tcria(4);
	Tinsere(sala4.conteudo, &envelope);
	Tinsere(sala4.conteudo, &foto);


	//SALA 5
	sala5.nome = "sala reflexão ";
	sala5.artigos = malloc(2*sizeof(string));
	sala5.artigos[0] = "a";
	sala5.artigos[1] = "uma";
	sala5.longa = "BEM-VINDO À REFLEXÃO .\n"
	"Ao entrar, a poeira instantaneamente o cega. Após alguns segundos, você consegue distiguinr alguns objetos.\n"
	"Em uma parede há um espelho. Sua limpeza destoa do resto da sala. Mesmo sem muito luz, você consegue enxergar sua reflexão perfeitamente.\n"
	"No canto mais empoirado da sala, você vê uma arma. Sua forma já se mistura com o ambiente, mas você consegue perceber a silhueta suave.\n Ninguém a toca em uma eternidade, aparentemente\n"
	"E, no outro extremo, uma figura raquítica e curva se senta ao chão, abraçando os joelhos e com os olhos baixos. A pele parece ter começado a se dissolver de tão velha, e os olhos não apresentam "
	"mais brilho algum. A vida já saiu deste homem.";

	sala5.curta = "Um homem, uma arma e um espelho. Não há nada mais aqui";
	sala5.ativo = False;
	sala5.visivel = True;
	sala5.conhecido = False;
	sala5.conteudo = Tcria(4);
	sala5.def.lugar.saidas[0] = &sala2;
	sala5.def.lugar.saidas[1] = &sala2;
	sala5.def.lugar.saidas[2] = &sala6;
	sala5.def.lugar.saidas[3] = &sala4;
	sala5.animacao = NULL;

	arma.nome = "arma";
	arma.artigos = malloc(2*sizeof(string));
	arma.artigos[0] = "a";
	arma.artigos[1] = "uma";
	arma.longa = "Incrustada de sujeira, ainda parece funcionar. O cano é tão longo quanto o de um revólver. É possível ver uma leve reflaxão no metal enferrujado por baixo da poeira.";
	arma.curta = "Uma arma velha, suja e enferrujada.";
	arma.ativo = True;
	arma.visivel = False;
	arma.conhecido = False;
	arma.conteudo = Tcria(4);
	arma.def.objeto.lista = NULL;
	arma.animacao = NULL;

	espelho.nome = "espelho";
	espelho.artigos = malloc(2*sizeof(string));
	espelho.artigos[0] = "o";
	espelho.artigos[1] = "um";
	espelho.longa = "No meio da sujeira da sala, a limpeza desde espelho surpreende. Você consegue ver as reflexões do ambiente claramente, e de uma forma elas acabam parecendo bonitas, "
	"apesar de toda a sujeira.\n"
	"Ao se aproximar dele, você se vê. Mas algo está faltando, só não é capaz de dizer o quê.";
	espelho.curta = "As reflexões trazem mais clareza para a sala do que ela mesma.";
	espelho.ativo = False;
	espelho.visivel = False;
	espelho.conhecido = False;
	espelho.conteudo = Tcria(4);
	espelho.def.objeto.lista = NULL;
	espelho.animacao = NULL;

	homem.nome = "homem";
	homem.artigos = malloc(2*sizeof(string));
	homem.artigos[0] = "o";
	homem.artigos[1] = "um";
	homem.longa = "É um homem, velho e fraco. As marcas do tempo são aparentes: as rugas, os ossos expostos, a dor. Não há brilho nos seus olhos nem força no seu corpo. Você duvida "
	"se ele sabe da sua presença, mas você sente a dele dentro de si. Um sentimento de angústia e desespero. Uma nostalgia doente. Um questionamento.";
	homem.curta = "Nada mais pode ser tirado observando-o.";

	homem.def.objeto.lista = malloc(4*sizeof(atrib));
	homem.def.objeto.lista[0].val = 1;
	homem.def.objeto.lista[2].val = 1;
	homem.ativo = False;
	homem.visivel = False;
	homem.conhecido = False;
	homem.conteudo = Tcria(4);
	homem.animacao = NULL;

	sala6.nome = "sala Hedonismo";
	sala6.artigos = malloc(2*sizeof(string));
	sala6.artigos[0] = "a";
	sala6.artigos[1] = "uma";
	sala6.longa = "BEM-VINDO AO HEDONISMO.\n"
	"Cores vivas fazem as paredes brilharem aos seus olhos, padrões que se misturam o fazem sentir em um oceano de luz.\n"
	"Um jardim dos mais diversos cogumelos cobre o chão da sala. Tamanhos, odores e cores. Nada parece fora do campo de possibilidades.\n"
	"Uma garrafa simples mas atraente senta ao lado de uma cama grande, que exala leveza. Tudo cheira a natureza.";
	//puts(sala6.longa);
	sala6.curta = "Uma imersão em natureza e sensações. Há muito para experimentar.";
	sala6.ativo = False;
	sala6.visivel = True;
	sala6.conhecido = False;
	sala6.conteudo = Tcria(4);
	sala6.def.lugar.saidas[0] = &sala3;
	sala6.def.lugar.saidas[1] = &sala3;
	sala6.def.lugar.saidas[2] = &sala4;
	sala6.def.lugar.saidas[3] = &sala5;
	sala6.animacao = NULL;
	Tinsere((sala5.conteudo), &homem);
	Tinsere(sala5.conteudo, &espelho);
	Tinsere(sala5.conteudo, &arma);

	garrafa.nome = "garrafa";
	garrafa.artigos = malloc(2*sizeof(string));
	garrafa.artigos[0] = "a";
	garrafa.artigos[1] = "uma";
	garrafa.longa = "Sua mente não consegue achar palavras para descrever o sentimento evocado dor essa garrafa. Sua beleza é simples, quase angelical.\n O líquido interno está em constante mudança, "
	"variando pelas mais diversas cores. Uma visão perturbadora e atraente.";
	garrafa.curta = "Seu conteúdo é um mistério, mas sua beleza é indescritível.";
	garrafa.ativo = False;
	garrafa.visivel = False;
	garrafa.conhecido = False;
	garrafa.conteudo = Tcria(4);
	garrafa.def.objeto.lista = NULL;
	garrafa.animacao = NULL;

	cama.nome = "cama";
	cama.artigos = malloc(2*sizeof(string));
	cama.artigos[0] = "a";
	cama.artigos[1] = "uma";
	cama.longa = "Uma cama de linho, com dois travesseiros de penas de ganso. Um cobertor vermelho feito do mais macio dos veludos. Uma armação gloriosa, digna de um rei.\n"
	"Algo que você nunca sonhou em ver.";
	cama.curta = "Parece muito macia.";
	cama.ativo = True;
	cama.visivel = True;
	cama.conhecido = False;
	cama.conteudo = Tcria(4);
	cama.def.objeto.lista = NULL;
	cama.animacao = NULL;

	cogumelos.nome = "cogumelos";
	cogumelos.artigos = malloc(2*sizeof(string));
	cogumelos.artigos[0] = "os";
	cogumelos.artigos[1] = "uns";
	cogumelos.longa = "Um jardim multicolor, multitamanho e multifragrância. Você nunca viu tanta diversidade em um só lugar. Cada cogumelo evoca uma emoção, uma sensação.\n"
	"É como ver infinitos novos jeitos de viver.";
	cogumelos.curta = "É impossível saber o que eles farão com você.";
	cogumelos.ativo = True;
	cogumelos.visivel = True;
	cogumelos.conhecido = False;
	cogumelos.conteudo = Tcria(4);
	cogumelos.def.objeto.lista = NULL;
	cama.animacao = NULL;
	Tinsere(sala6.conteudo, &cama);
	Tinsere(sala6.conteudo, &cogumelos);
	Tinsere(sala6.conteudo, &garrafa);
}
