%Capítulo 14 questão 8) c

%parâmetros colocados da tabela 14.2
k = -5:1:-1;
h = 10.^k;
h1 = h;
h0 = h1/2;

%x-1 (x minus 1)
xm1 = 0;
x0 = xm1 + h0;
x1 = x0 + h1;


function y = f(x)
  y = exp(x);
endfunction

  
%Método 1:
g1 = (f(x1) - f(x0))./h1;   %g1/2
g2 = (f(x0) - f(xm1))./h0;  %g-1/2

meth1 = (g1 - g2)./((h0+h1)./2);

%Metodo 2:
f0 = (f(x0) - f(xm1))./h0;  %f[x-1,x0]
f1 = (f(x1) - f(x0))./h1;  %f[x0,x1]
%diferença dividida f[x-1, x0, x1]
df = (f1 - f0)./(x1 - xm1);

meth2 = 2.*df;

exact = 1;

format long g
err1 = abs(meth1-exact)
err2 = abs(meth2-exact)

%{

  Com esses resultados empíricos, podemos observar com mais clareza que,
  de fato, os dois métodos são o mesmo, 
  Tanto pela implementação muito parecida que explicita essa igualdade,
  quanto pelos resultados (iguais)
  
  Além disso, podemos perceber o caráter de primeira ordem do erro,
  isto é, linearmente proporcional a ordem de h.

%}