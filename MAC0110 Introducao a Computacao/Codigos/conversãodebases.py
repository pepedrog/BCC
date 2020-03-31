
def decodifica(x,base):
    """ converte o código x da base para um valor inteiro.
    """
    s = 0
    potencia = 1
    while x>0:
        digito = x%10
        termo = digito*potencia
        s = s+termo
        potencia = potencia*base
        x = x//10
    return s

def codifica(valor,base):
    """ converte o valor inteiro para a base.
    """
    x = 0
    potencia = 1
    while valor>0:
        resto = valor % base
        termo = resto*potencia
        x = x+termo
        potencia = 10*potencia
        valor = valor // base
    return x

x = int(input("Digite um valor codificado: "))
base = int(input("Digite a base de codificação: "))
valor = decodifica(x,base)
print("(",x,") na base ",base," é igual a ",valor,sep='')
base2 = int(input("Digite a base para recodificação: "))
x2= codifica(valor,base2)
print(valor," é igual a (",x2,") na base ",base2,sep='')


