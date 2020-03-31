#Estamos usando a função rnd do exercício 3
xi = [1, 1, 1, 1, 1, 1, 1, 1, 1, 2];
n = 10;
media = sum(xi)/n;

soma1 = 0;
for i = (1:1:5)
  soma1 += rnd((xi(i) - media)^2, 2);
  soma1 = rnd(soma1, 2);
  
endfor

sigma1 = rnd(soma1/n, 2)

sigma2 = rnd((sum(xi.^2))/n, 2) - rnd(media^2, 2)

#{
Este exemplo bem bobo já nos mostra como 
A segunda forma de calcular nos previniu de um erro, isso contando com apenas 2 casas decimais
Podemos explicar pelo fato de que a média pode ser muito próxima de vários termos,
Então fazer essa diferença tantas vezes nos deixa em uma margem de muitos erros de cancelamento!
#}