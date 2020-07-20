"""
Script principal, que chama as funcoes dos outros modulos para
carregar os dados, fazer o pre-processmanto e adequacao, instanciar
uma rede neural Feed-Foward com 2 camadas ocutas e treina-la, utilizando
os dados processados para prever se chovera amanha,
dados os valores de features meteorologicas selecionadas.
Salva tambem o modelo em disco e abre um menu iterativo para a utilizacao
exploratoria do  modelo.
"""

from model import FFN_2HLayers
from train import split_data, train_network
from results import save_results
import torch
import pandas as pd

N_HL1 = 10
N_HL2 = 10
LEARNING_RATE = 0.001

if __name__ == "__main__":
    
    path = '../PRE/dados_final/'
    nns = [('TODOS OS EXAMES', 'einstein_processed_all.csv', 3),
           ('APENAS PCR', 'einstein_processed_pcr.csv', 1),
           ('APENAS IGG', 'einstein_processed_igg.csv', 1),
           ('APENAS IGM', 'einstein_processed_igm.csv', 1)]
    
    results = []
    for nn in nns:    
        print('REDE NEURAL - ' + nn[0])
        processed_data = pd.read_csv(path + nn[1])
        
        print('ADEQUANDO DADOS PARA TREINAMENTO...')
        splitted_data = split_data(processed_data)
    
        print('MONTANDO MODELO...')
        x_train = splitted_data[0]
        network = FFN_2HLayers(x_train.shape[1], N_HL1, N_HL2, nn[2])
        optimizer = torch.optim.Adam(network.parameters(), lr=LEARNING_RATE)
        criterion = torch.nn.BCELoss()
    
        print('TREINANDO...')
        acc = train_network(splitted_data, 10, network, optimizer, criterion)
        
        results.append(acc)
        
        print('---------------------------------------------- ')
    
    save_results(results)
    
    print('FIM.')