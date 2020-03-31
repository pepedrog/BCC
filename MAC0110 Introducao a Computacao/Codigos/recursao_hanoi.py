

def hanoi(n,origem,destino):
    """ Exemplo de aplicação de recursão: Torres de Hanoi O objetivo é
        passar n discos da posição "origem" para a posição
        "destino". A base da recursão é quando há um só disco e a
        transferência é feita diretamente.  Do contrário, transfere-se
        recursivamente os n-1 discos do topo da posição origem para
        uma posição temporária, transfere-se o disco n diretamente da
        origem para o destino, e finalmente transfere-se os n-1 discos
        da posição temporária para a posição destino.
    """
    if n==1: # base da recursão... n=1 é fácil!
        print("Transfira o disco 1 da posição",origem,"para a posição",destino)
        return
    temporario = 6-origem-destino # calcula a posição que está livre
    hanoi(n-1,origem,temporario)
    print("Transfira o disco",n,"da posição",origem,"para a posição",destino)
    hanoi(n-1,temporario,destino)

# testes
print("Torres de Hanoi: transferindo 4 discos da posição 1 para a posição 3")
hanoi(4,1,3)

