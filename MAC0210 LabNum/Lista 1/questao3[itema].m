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