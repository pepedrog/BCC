
Existem três "front-ends" ({cli,tk,g}geocomp.py). Para rodar qualquer
um deles, você vai precisar de Python (testado com aa versão 3.5.4,
mas 3.x.x deve funcionar).  Além disso, tkgeocomp.py precisa do módulo
padrão de Tk que acompanha a distribuição de Python. O módulo
ggeocomp.py atualmente não está funcionando, pois o pacote que esse
módulo usava (gnome-python) não parece ser mais suportado.

O arquivo geocomp/config.py pode ser alterado para mudar cores, tamanho
da janela, largura da linha, etc.

O programa tenta carregar automaticamente o primeiro arquivo do
diretório "dados". Depois disso, é possível abrir arquivos em outros
diretórios, usando o "menu" na parte superior esquerda da tela.

Depois de rodar um algoritmo, o programa mostra o número de operações
primitivas realizadas pelo algoritmo ao lado do seu botão. Alguns
algoritmos podem retornar informações adicionais que são mostradas na
parte inferior da janela.

O tempo entre dois passos de um algoritmo pode ser alterado
dinamicamente durante a sua execução e também é possível executar apenas
uma pequena parte do algoritmo passo a passo, bastando para isso usar
o botão "passo a passo". Algumas vezes, é desejável apenas medir a
eficiência de um algoritmo para uma determinada entrada. Como qualquer
algoritmo leva mais tempo desenhando do que fazendo conta, é possível,
antes de iniciar um algoritmo, apertar o botão "esconder" para não
desenhar nada na tela, permitindo que o algoritmo rode bem mais rápido.

O front-end tkgeocomp.py permite salvar a imagem que está desenhada
em um determinado instante na tela, bastando para isso apertar o botão
"imprimir". O formato da imagem criada é .eps (Encapsulated Postscript).

O front-end ggeocomp.py permite dar um zoom em uma determinada área da
tela - infelizmente esse zoom não é muito útil porque os pontos
continuam sendo desenhados na mesma proporção.

O front-end cligeocomp.py pode ser usado para rodar os algoritmos não
interativamente. Ele pode ser chamado como:
	cligeocomp geocomp/closest/brute.py dados/LOOSE_PTS/ptos*
para rodar o algoritmo de par de pontos mais próximo em todos os arquivos dados/LOOSE_PTS/ptos*.


Acrescentando novos algoritmos/problemas
========================================
Para acrescentar um novo algoritmo de, por exemplo, par de pontos mais próximo:
- escreva seu algoritmo no arquivo geocomp/closest/novo_alg.py, numa
  função Novo_alg
- edite geocomp/closest/__init__.py colocando uma linha
	import novo_alg
  e adicione um item 
  ('novo_alg', 'Novo_alg', 'um nome para aparecer na interface grafica')
  à variável children

Para colocar um novo problema:
- crie um diretório geocomp/novo_problema
- crie geocomp/novo_problema/__init__.py , no mesmo estilo de
  geocomp/closest/__init__.py :
  - uma linha "import foo" para cada arquivo foo.py
  - uma lista "children" que possui um item 
  ( 'foo', 'Funcao_de_Foo', 'Nome para a interface grafica')
    para cada arquivo foo.py em geocomp/closest/
- edite geocomp/__init__.py e coloque uma linha:
	import novo_problema
  e coloque um item
  ( 'novo_problema', None, 'Um nome para a interface grafica')
  na variável children

Se o novo problema possuir uma entrada que não seja um conjunto de
pontos, será necessário alterar, pelo menos geocomp/common/io.py e
geocomp/common/guicontrol.py (função run_algorithm) para que tudo
funcione.


Dúvidas, contate:

 - alexis at ime dot usp dot br ( Alexis Sakurai Landgraf, criador
  original do arcabouço)
 
 - victorsp at ime dot usp dot br (Victor, responsável pela adaptação
   para python3)


