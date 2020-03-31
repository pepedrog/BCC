% Capítulo 15 questão 7

% Especificações do exercício

ri = [2 4 8 16 32 64];

% Funções a serem integradas
function y = f1(x)
  y = 4/(1+x*x);
endfunction 
exact1 = pi;

function y = f2(x)
  y = sqrt(x);
endfunction 
exact2 = 2/3;

% Método do ponto intermediário composto
function y = CompMidPoint(f, a, b, r)  
  h = (b-a)./r;
  i = 1:1:r;
  
  %x[i] = (t[i] + t[i-1])/2 = (a + ih + a + (i-1)h)/2 = a + (i-1/2)h
  x = a + h.*(i - .5);
  
  sumx = 0;
  for i = 1:1:r
    sumx += f(x(i));
  endfor
  y = h*sumx;
  
endfunction

% Método trapezoidal composto
function y = CompTrapezoidal(f, a, b, r)
  h = (b-a)./r;
  i = 1:1:r-1;
  t = a + h.*i;
  sumt = 0;
  for i = 1:1:r-1
    sumt += f(t(i));
  endfor
  y = h/2 * (f(a) + 2*sumt + f(b));
  
endfunction

% Método de Simpson composto
function y = CompSimpson(f, a, b, r)
  h = (b-a)./r;
  i = 1:1:r;
  t = a + h.*i;
  
  %s1 é a soma dos pontos medios
  %inicializada com f((t[0] + t[1])/2)
  s1 = f((a + t(1))/2);
  
  %s2 é a soma dos t[i], i = 1,..,r-1
  s2 = 0;
  
  for i = 2:1:r
    s1 += f((t(i-1) + t(i))/2);
    s2 += f(t(i-1));
  endfor

  y = (h/6)*(f(a) + 4*s1 + 2*s2 + f(b));
  
endfunction

% Primeira função %

error1 = [];
error2 = [];
error3 = [];

%Pra cada r

for i = 1:1:6
  r = ri(i);
  errMid =  abs(exact1 - CompMidPoint(@f1, 0, 1, r));
  errTrap = abs(exact1 - CompTrapezoidal(@f1, 0, 1, r));
  errSimp = abs(exact1 - CompSimpson(@f1, 0, 1, r));
  
  error1 = [error1 errMid];
  error2 = [error2 errTrap];
  error3 = [error3 errSimp];
  
endfor

subplot(2,1,1)
semilogy(ri,error1, ri, error2, ri, error3)
hold on
legend('Midpoint', 'Trapezoidal', 'Simpson')

xlabel('r')
ylabel('absolute error')

% Segunda função

error1 = [];
error2 = [];
error3 = [];
%Pra cada r
for i = 1:1:6
  r = ri(i);
  errMid =  abs(exact2 - CompMidPoint(@f2, 0, 1, r));
  errTrap = abs(exact2 - CompTrapezoidal(@f2, 0, 1, r));
  errSimp = abs(exact2 - CompSimpson(@f2, 0, 1, r));
  
  error1 = [error1 errMid];
  error2 = [error2 errTrap];
  error3 = [error3 errSimp];
  
endfor

subplot(2,1,2)
semilogy(ri,error1, ri, error2, ri, error3)
hold on
legend('Midpoint', 'Trapezoidal', 'Simpson')

xlabel('r')
ylabel('absolute error')


%{

  Análise dos resultados empíricos + teoricos vistos em aula/livro:
    
  Nos gráficos plotados ficam mais claras algumas conclusões
  Como, por exemplo, o interessante paralelismo entre os metodos
  do midpoint e do trapezoidal:
     O trapezoidal tem erro que é sempre o dobro do do midpoint
     Isso é uma conclusão teórica que tivemos em aula, e que pode ser comprovada
     nesses resultados
  Além disso, o método do midpoint, além de mais acurado é ligeiramente mais barato
  Enquanto no trapezoidal fazemos r + 1 avaliações de f, 
  no midpoint fazemos r (1 a menos)
  
  Já quando comparamos com o método de Simpson, percebemos, principalmente
  no primeiro exemplo, que o erro do simpson é de uma ordem de grandeza maior que
  os dois primeiros
  
  Porém, essa precisão tem um custo expressivamente maior, fazendo
  4r + 2(r-1) + 2 = 6r avaliações de função

  Enfim, a precisão invejável da Regra de Simpson tem um custo que pode sair muito caro
  Já o método do midpoint fornece uma aproximação mais barata e mais precisa que a trapezoidal
  
  Como os graficos são log10 e o r tem proporção log2, os gráficos não ficam tão estéticos
  Mas é possivel visualizar que a ordem das primeiras aproximações são iguais,
  e que a de Simpson é maior
  

}%