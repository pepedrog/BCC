soma1 = soma2 = soma3 = 0;
#Forma 1:
#Implementação direta
for n = (1:1:10000)
  soma1 += 1/n;
endfor

#Forma 2:..
#Implementação arredondada
for n = (1:1:10000)
  soma2 += rnd(1/n, 5);
  #Linha para garantir que a soma nunca tera mais que 5 dígitos decimais
  soma2 = rnd(soma2, 5);
endfor

#Forma 3:
#Implementação arredondada inversa
for n = (10000:-1:1)
  soma3 += rnd(1/n, 5);
  soma3 = rnd(soma3, 5);
endfor

#{
  soma1 = 9.787606036
  soma2 = 9.7108
  soma3 = 9.7913
  
  Verificamos que a soma3 é muito mais precisa que a soma2
  
  Explicamos isso com a representação dos números:
  Quando começamos dos maiores (caso 2) obtemos rapidamente as 5 casas decimais mais significativas
  Assim, quando chegamos nas iterações posteriores, nosso sistemas com poucas casas simplesmente desconsidera
  os valores menores, menores que 10^-6 por exemplo
  
  Já quando começamos pelos menores, obtemos digitos pequenos que vão se acumulando, pois ainda fazem parte dos mais signifoicativos
  Quando vamos aos maiores, já temos um acumulado que explica essa precisão maior
  
  Podemos perceber que o erro da soma3 é causado muito mais pelos arredondamentos,
  Já na soma 2 erramos por desprezar os valores, não por arredondá-los 

#}