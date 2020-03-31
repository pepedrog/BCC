#definindo x0 e h
x0 = 1.2;
h = 10.^(-1:-1:-7);
#df = valor que gostariamos de obter para derivada do sin(x0)
df = cos(x0);

#vetor que obteremos para cada h
aproximacao = ((sin(x0 + h) - sin(x0 - h))./(2*h));
abs_err = abs(df - aproximacao);

disp("   h            erro absoluto")
disp([h; abs_err]')

#{
  Comentários sobre o erro
  No cálculo do livro, onde o erro é proporcional à h/2*f''(x0),
  temos que o erro pode ser aproximado por e1 = h*(-0.466)
  
  Nesse caso, onde o erro é proporcional à h²/6*f'''(x0)
  temos que o erro pode ser aproximado por e2 = h²*(-cos(x0)/6) = h²*(-0.166)

  Com uma estimação um pouco grosseira, podemos estabelecer que
  |e2| ~= |e1²|, se considerarmos que o h é o fator mais influente
  calcular o valor de ambos os erros, pois ele que define a ordem de grandeza
  Podemos ainda inferir que e2 << e1² pois a constante de e2 (-0.16) é notávelmente menor que a de e1 (-0.46)
  
  Isso explica muito bem os valores obtidos, onde a ordem de grandeza de e2 é em geral o dobro de e1
  ou seja, quando e1 = 10^-4, e2 < e1² = 10^-8. E assim sucessivamente.

#}
