% Capítulo 15 questão 4) b

a = 0;
b = 1;

% f(x) = f'(x) = exp(x)
function y = f(x)
  y = exp(x);
endfunction

%I = regra trapezoidal corrigida
function y = I(a, b)
  y = (b-a)*(f(a) + f(b))/2 + ((b-a)^2)*(f(a) - f(b))/12;
endfunction

%Integral exata
function y = exact(a, b)
  y = f(b) - f(a);
endfunction

err1 = abs(exact(a, b) - I(a, b))
a = 0.9;
err2 = abs(exact(a, b) - I(a, b))

%{
  
  Rodando esse código, conseguimos os erros
  err1 = 0.0025 = 2.5 e-3
  err2 =          3.5 e-8
  
  Ao compararmos com o exemplo 15.2, a primeira coisa que percebemos
  é a semelhança do erro dessa regra com a regra de Simpson
  Com ordens de grandeza muito semelhantes 
  
  Isso se deve ao fato do erro de truncamento teorico das duas aproximaçõesse
  terem a mesma ordem (b-a)^5
  Além da ordem, podemos ver que o coeficiente do erro teorico da regra de simpson
  é precisamente 4 vezes maior que o da trapezoidal corrigida, surpreendentemente 
    (90*2^5) = 2880 = 4*720 
    
  E essa relação é razoavelmente mantida nos nossos resultados empíricos
  na regra de simpson do exemplo temos
  errS1 = 6e-4 ~= 2.4e-3 / 4 ~= err1 / 4
  errS2 = 9e-9 ~= 3.6e-8 / 4 ~= err2 / 4
  
  Podemos ver que regra de simpson é mais precisa, porém demanda a avaliação da função em 3 pontos
  Já a trapezoidal corrigida demanda a avaliação de 2 pontos da função + 2 da derivada nos mesmos pontos
  Ou seja, cada aproximação pode ser melhor dependendo do contexto
  
%}