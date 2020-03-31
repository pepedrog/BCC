testes = (1:100:1e6);

function y = f1(x)
  y = log(x - sqrt(x.^2 - 1));
endfunction

function y = f2(x)
  y = -log(x + sqrt(x.^2 - 1));
endfunction

erro = abs(f1(testes) - f2(testes));
max(erro)

plot (testes, erro,'.');

title('questão 5 b')
xlabel('testes')
ylabel('error')

#{
  Com esses exemplos, podemos ver que o erro pode ficar relativamente grande (10^-4)
  Isso é, apenas 4 casas decimais de coincidencia dos cálculos.

  Sobre a precisão, devemos novamente ressaltar a influencia dos erros de cancelamento e arredondamento
  Em geral, no calculo 1 estamos sujeitos ao cancelamento pelo fato de haver dois numeros que podem ser de hgrandezas muito diferentes sendo subtraídos
  Já com a soma, o máximo que pode ocorrer é deixarmos de somar algo muito pequeno, sendo menos grave.

  Isto é, a segunda forma de calcular apresenta maior acurácia.  


#}