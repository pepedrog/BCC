% Examples 1.2--1.3 and Figure 1.3

x0 = 1.2;
fp = cos(x0);
i = -20:0.5:0;
h = 10.^i;
#Calculando o erro com a nossa definição da derivada
err = abs (fp - (sin(x0+h) - sin(x0 - h))./(2*h) );

#Conforme explicado no exercício anterior (1 b) o erro para nossa aproximação
#é dado por |h²/6 * f'''(x0)| = |- cos(x0)/6 * h²|
d_err = (cos(x0)/6)*(h.^2);

#plotando o gráfico igual ao exemplo
loglog (h,err,'-*');
hold on
loglog (h,d_err,'r-.');
xlabel('h')
ylabel('Absolute error')
axis([10^(-20) 1 10^(-15) 1])

#{
  Nosso exercício se comportou de modo muito similar ao exemplo do livro!
  Podemos ver que o erro segue o valor esperado de modo muito preciso
  Acompanhando de perto a previsão calculada, que decresce muito mais rápido que o exemplo do livro!
  
  Então, quando existe um momento em que os erros de aproximação são superados pelos erros de cancelamento,
  pois os valores ficam tão pequenos que, quando calculamos f(x0 + h) - f(x0 - h) obtemos algo muito próximo de 0
  Assim, esse erro da subtração domina o restante do cálculo, fazendo o erro disparar e perdendo a proporcionalidade esperada.
  
  No nosso exemplo isso ocorre quando h está próximo de 1e-5, diferentemente do do livro, onde isso ocorre em 1e-7
  Por outro lado, nosso erro atinge um mínimo menor que o do livro (1e-12 contra 1e-9)
  Isso poe ser explicado pela proporcionadade do nosso erro:
    Quando o h está pequeno no exemplo do livro, o erro acompanha essa ordem de grandeza
    Mas no nosso exercício, quando h está pequeno, o erro está em uma ordem proporcial ao dobro da de h
    Assim, o erro de cancelamento aparece muito mais rápido (com h menor)

#}