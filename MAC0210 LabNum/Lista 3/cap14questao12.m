%Capítulo 14 questão 12

k = -8:.5:0;
h = 10.^k;

x0 = 1.2;
x1 = x0 + h; %x1
x2 = x0 - h; %x-1

%f(x) = sen(x)
function y = f(x)
  y = sin(x);
endfunction

f0 = f(x0);
f1 = f(x1);
f2 = f(x2);

fpp0 = (f1 - 2*f0 + f2)./(h.^2);

%f''(x) = -sen(x)
exact = -sin(1.2);
error = abs(exact - fpp0)

loglog(h,error)
xlabel('h')
ylabel('absolute error')

%{
  
  Observando o gráfico/ os resultados obtidos podemos perceber a proporção entre
  o erro e o quadrado do h
  isto é, o expoente do erro é proporcional ao dobro do expoente do h
  
  Isso vale até os erros de aproximação dominarem a conta
  Após isso acontecer, podemos ver que o erro começa a aumentar,
  porém como vimos na expressão teórica, os erros de arrendodamento
  também são proporcionais a h²
  
  Isso explica o formato em V do gráfico
  Para h maiores, o erro decai proporcionalmente a h²
  para h menores, o erro cresce com a mesma proporção, ou seja, uma espécie de simetria
  
  Com uma breve observação, podemos perceber que o mínimo erro obtido ocorre com h ~= 1e-4
  
%}