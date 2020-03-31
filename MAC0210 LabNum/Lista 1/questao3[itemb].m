#Código adaptado do exemplo 2.2
#{
#Função do exercício anterior (se precisar 'recompilar' só descomentar)
function y = rnd(x, n)
	#Definindo qual a ordem de grandeza e a parte que precisaremos subtrair
  #ordem de grandeza de x
  ordemx = 0;
  while(10**ordemx < x)
    ordemx += 1;
  endwhile
  
  #Ordem de grandeza dos dígitos que retiraremos
	ordem = 10^ (-n + ordemx);
	resto =  mod(x, ordem);
	#Tira todos os digitos posteriores a ordem desejada
	y = x - resto;
	#Confere se o primeiro dígito depois do truncamento é maior que 5,
	#Se sim, incrementamos 1 na ultima casa, para arredondar
	if((resto > ordem/2))
		y = y + ordem;
		
	endif
endfunction
#}

#{
  A relação entre a unidade de arredondamento n e a escala vertical 
  é muito direta.
  Podemos perceber que o maior erro que podemos cometer é algo em torno de 1/2 * 10^(-n)
  Pois esse é o erro que assumimos a fazer o arredondamento
  Assim, os valores do eixo y estão diretamente ao redor de 10^(-n)   
#}

t = 0:.002:1;
tt = exp(-t) .* (sin(2*pi*t)+2);
rt = rnd(tt, 5);
round_err = (tt - rt) ./tt ;
plot (t,round_err,'b-');
title('error in sampling exp(-t)(sin(2\pi t)+2) in precision n = 5')
xlabel('t')
ylabel('roundoff error')

% relative error should be about eta = eps(single)/2
rel_round_err = max(abs(round_err)) / (10^(-5)/2)