
x0 = 1.2;
fp = cos(x0);
i = -30:1:0;
h = 10.^i;
#Calculando o erro com a nossa nova definição de derivada
#{
  f(x0 + h) - f(x0) = sin(x0 + h) - sin(x0) =
  2*cos((x0 + h + x0)/2)*sin((x0 + h - x0)/2) = 2*cos(x0 + h/2)*sin(h/2)
#}
err = abs((fp - (2*cos(x0 + h/2).*sin(h/2))./h));

#{
  Aqui eu tive que lidar com um problema:
  A partir do h < 10^-16 o erro estava sendo == 0
  O que é ótimo!
  Mas, obtiamos um warning, pois o 0 não é representado no grafico loglog
  Então, apenas para a visualização gráfica ficar mais interessante,
  quando o erro for 0, vamos colocar na base do gráfico (1e-20) 
#}
for i = (1: 1: 30);
  if(err(i) == 0) 
    err(i) = 1e-30;
  endif
endfor
   
loglog (h,err,'-*');
xlabel('h')
ylabel('Absolute error')
axis([10^(-30) 1 10^(-30) 1])
