'''
Programa que implementa as funcoes necessarias para o treinamento do modelo
definido em model.py, utilizando os dados ja pre-processados pelos
procedimentos definidos em data.py.
Esse programa implementa a funcao principal de treinamento, funcoes de
preparacao dos dados ao trainamento e funcoes auxiliares, utilizadas no
processo de treinamento.
'''


import torch
import pandas as pd
from sklearn.model_selection import KFold

RANDOM_SEED = 42
torch.manual_seed(RANDOM_SEED)

# FUNCOES AUXILIARES
def calculate_accuracy(y_true, y_pred):
    """Funcao que calcula a acuracia de uma previsao"""
    predicted = y_pred.ge(.5)  # Binariza a previsa
    # Rede neural com todos os exames: 
    if len(y_true.size()) > 1:
        pcr = (y_true[:, 0:1] == predicted[:, 0:1]).sum().float() / len(y_true)
        igg = (y_true[:, 1:2] == predicted[:, 1:2]).sum().float() / len(y_true)
        igm = (y_true[:, 2:3] == predicted[:, 2:3]).sum().float() / len(y_true)
        return pcr.item(), igg.item(), igm.item()
    # Rede neural com só um exame: 
    acc = (y_true == predicted).sum().float() / len(y_true)
    return acc.item()
    
# FUNCOES DE ADEQUACAO
def split_data(pp_data):
    """Funcao que realiza a adequacao final dos dados para o uso pela rede"""
    # Separa as features das variaveis-alvo
    target = ['Resultado COVID-19:', 'COVID IgG Interp', 'COVID IgM Interp']
    target = list(set(target).intersection(set(pp_data.columns)))
    features = list(set(pp_data.columns) - set(target))
    x = pp_data[features]
    y = pp_data[target]
    
    # Transforma todos os conjuntos em tensores do PyTorch:
    x = torch.from_numpy(x.to_numpy()).float()
    y = torch.squeeze(torch.from_numpy(y.to_numpy()).float())
    
    return (x, y)

def transfer_to_device(data, network, criterion):
    '''Funcao auxiliar que transfere todos os objetos a serem usados no
    treinamento para o mehor dispositivo disponivel para o seu processamento'''
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    (x_train, y_train, x_val, y_val) = data

    x_train = x_train.to(device)
    y_train = y_train.to(device)

    x_val = x_val.to(device)
    y_val = y_val.to(device)

    network = network.to(device)
    criterion = criterion.to(device)

    trasfered_data = (x_train, y_train, x_val, y_val)
    return (trasfered_data, network, criterion)

def split_k_fold(x, y, k):
    """ Separa os dados de entrada e saída de acordo com o treinamento i do k_fold """
    kf = KFold(k)
    
    train_x = []
    test_x = []
    train_y = []
    test_y = []
    for train_index, test_index in kf.split(x):
        train_x.append(x[train_index])
        test_x.append(x[test_index])
        train_y.append(y[train_index])
        test_y.append(y[test_index])
    
    return train_x, test_x, train_y, test_y

def train_network(data, k, network, optimizer, criterion):
    """ Treina a rede neural usando a técnica de k-folds, com os dados e parâmetros fornecidos """

    (x, y) = data
    x_train, x_val, y_train, y_val = split_k_fold(x, y, k)
    
    rows = []
    for i in range(k):
        data_k = (x_train[i], x_val[i], y_train[i], y_val[i])
        
        i_result = train_fold(data_k, network, optimizer, criterion)
        
        if isinstance(i_result[1], tuple):
            values = [i_result[0], i_result[1][0], i_result[1][1], i_result[1][2]]
        else:
            values = [i_result[0], i_result[1]]
        rows.append(pd.DataFrame([values]))
        
    results = pd.concat(rows, ignore_index = True)
    if len(results.columns) == 4:
        results.columns = ['loss', 'acc pcr', 'acc igg', 'acc igm']
    else:
        results.columns = ['loss', 'acc']
    return results
    
# FUNCAO PRINCIPAL DE TREINAMENTO:
def train_fold(data, network, optimizer, criterion):
    """Funcao que realiza o treinamento de uma rede neural, usando dados,
    funcao e criterio de otimizacao fornecidos, salvando o modelo treinado
     em disco"""

    (data, network, criterion) = transfer_to_device(data, network, criterion)
    (x_train, x_val, y_train, y_val) = data
    
    # O treinamento consiste na repeticao  do cilo foward-backward atraves
    # do conjunto de treinamento, repetidas vezes (epocas):
    for epoch in range(1000):
        y_pred = network(x_train)  # faz-se a previsao
        y_pred = torch.squeeze(y_pred)
        train_loss = criterion(y_pred, y_train)  # calcula-se o custo
        optimizer.zero_grad()  # zera os gradientes do otimizador
        train_loss.backward()  # faz a passagem de volta
        optimizer.step()  # atualiza os parametros
        
    # Retorna os resultados
    y_val_pred = network(x_val)
    y_val_pred = torch.squeeze(y_val_pred)
    
    val_loss = criterion(y_val_pred, y_val).item()
    val_acc = calculate_accuracy(y_val, y_val_pred)
    
    return val_loss, val_acc
