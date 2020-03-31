%Capítulo 14 questão 2) b

k = -9:1:-1;
h = 10.^k;

%apenas facilitando a notação das funções
% f(x) = exp(x)
function y = f(x)
  y = exp(x);
endfunction

%minha aproximação de f'''(x)
function aprox = f3(x, h)
  aprox = (f(x + 2*h) - 2*f(x + h) + 2*f(x - h) - f(x - 2*h))./(2*(h.^3));
endfunction


aprox = f3(0, h)
error = abs(1 - aprox)

loglog(h,error)
xlabel('h')
ylabel('absolute error')

%{

 A melhor aproximação para f'''(0) = 1 que obtivemos foi com h = 10^-3 
 Quando tivemos a aproximação com erro de ordem 10⁻7
 
 Pudemos ainda perceber o caráter de segunda ordem dessa aproximação
 h        erro
 1e-1     2.5e-3
 1e-2     2.5e-5
 1e-3     2.5e-7
 
 Podemos ver como o expoente cresce proporcional ao quadrado de h
 Mais precisamente, algo em torno de h²/4 
 Que é nossa estimativa de ordem do erro
  
 Para h menores, os erros de truncamento perdem relevancia
 e começam a dominar os caóticos erros de arredondamento
 
%}