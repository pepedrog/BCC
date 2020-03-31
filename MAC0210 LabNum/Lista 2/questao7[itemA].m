function abc = quad(a, b, f, n, dfa)
  
%função que recebe uma função f um intervalo [a,b], n observaçoes (xi, yi) 
%e cria um polinomio interpolador por trechos quadráticos
%em n intervalos, sendo conhecido f'(a) = dfa

%Retorna uma matriz [ai, bi, ci]

h = (b - a)/n;
xi = a;
dfAnterior = dfa;
%em cada um dos n intervalos
for i = 1:n
  %a = f(xi) adiciona no fim do vetor
  ai(i) = f(xi);
  %b = f'(xi)
  bi(i) = dfAnterior;
  %c = f[x0, x1, x2] = f[x1,x2] - f[x0,x1] / 2*h
  ci(i) = ((f(xi+h) - f(xi))/h - dfAnterior)/ h;
  %Atualiza a derivada da extremidade direita (xi+1) 
  dfAnterior = bi(i) + 2*ci(i)*h;
  xi += h;
 end
 
 abc = [ai;bi;ci];