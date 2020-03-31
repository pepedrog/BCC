
def gcs(S,T):
    """ encontra a maior subsequência comum
        (greatest common subsequence) às strings S e T.
    """
    # t representa o tamanho da subsequência
    for t in range(len(S),-1,-1):
        for i in range(len(S)-t+1):
            j = i+t
            for k in range(len(T)-t+1):
                l = k+t
                if S[i:j]==T[k:l]:
                    return i, j, k, l

S = input("Digite a primeira frase: ")
T = input("Digite a segunda frase: ")
i,j,k,l = gcs(S,T)
print("A maior subsequência comum é '",S[i:j],"' que ocorre na primeira frase entre os índices ",i," e ",j-1," e na segunda frase entre os índices ",k," e ",l-1)

