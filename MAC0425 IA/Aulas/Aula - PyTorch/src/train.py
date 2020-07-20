'''
Programa que implementa as funcoes necessarias para o treinamento do modelo
definido em model.py, utilizando os dados ja pre-processados pelos
procedimentos definidos em data.py.
Esse programa implementa a funcao principal de treinamento, funcoes de
preparacao dos dados ao trainamento e funcoes auxiliares, utilizadas no
processo de treinamento.
'''


import torch
from sklearn.model_selection import train_test_split

RANDOM_SEED = 42
torch.manual_seed(RANDOM_SEED)


# FUNCOES AUXILIARES
def calculate_accuracy(y_true, y_pred):
    """Funcao que calcula a acuracia de uma previsao"""
    predicted = y_pred.ge(.5).view(-1)  # Binariza a previsao
    return (y_true == predicted).sum().float() / len(y_true)


def round_tensor(t, decimal_places=3):
    """Funcao que arredonda as componentes de um tensor para melhor visualizacao"""
    return round(t.item(), decimal_places)


# FUNCOES DE ADEQUACAO
def split_data(pp_data, val_size=0.2, r_seed=RANDOM_SEED):
    """Funcao que realiza a adequacao final dos dados para o uso pela rede"""
    # Separa as features da variavel-alvo:
    x = pp_data[['Rainfall', 'Humidity3pm', 'RainToday', 'Pressure9am']]
    y = pp_data[['RainTomorrow']]

    # Separa os conjutos de validacao e treinamento:
    x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=val_size,
                                                      random_state=r_seed)
    # Transforma todos os conjuntos em tensores do PyTorch:
    x_train = torch.from_numpy(x_train.to_numpy()).float()
    y_train = torch.squeeze(torch.from_numpy(y_train.to_numpy()).float())
    x_val = torch.from_numpy(x_val.to_numpy()).float()
    y_val = torch.squeeze(torch.from_numpy(y_val.to_numpy()).float())

    return (x_train, y_train, x_val, y_val)


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


# FUNCAO PRINCIPAL DE TREINAMENTO:
def train_network(data, network, optimizer, criterion,
                  MODEL_PATH='FFN_2HLayers_weather.pt'):
    """Funcao que realiza o treinamento de uma rede neural, usando dados,
    funcao e criterio de otimizacao fornecidos, salvando o modelo treinado
     em disco"""

    (data, network, criterion) = transfer_to_device(data, network, criterion)
    (x_train, y_train, x_val, y_val) = data

    # O treinamento consiste na repeticao  do cilo foward-backward atraves
    # do conjunto de treinamento, repetidas vezes (epocas):
    for epoch in range(1000):
        y_pred = network(x_train)  # faz-se a previsao
        y_pred = torch.squeeze(y_pred)
        train_loss = criterion(y_pred, y_train)  # calcula-se o custo
        # Imprime resutados parciais:
        if epoch % 100 == 0:
            train_acc = calculate_accuracy(y_train, y_pred)
            y_val_pred = network(x_val)
            y_val_pred = torch.squeeze(y_val_pred)
            val_loss = criterion(y_val_pred, y_val)
            val_acc = calculate_accuracy(y_val, y_val_pred)

            tr_lss = round_tensor(train_loss)
            tr_acc = round_tensor(train_acc)
            vl_lss = round_tensor(val_loss)
            vl_acc = round_tensor(val_acc)

            print('EPOCH {0}:'.format(epoch))
            print('Train Set --- loss:{0}; acc:{1}'.format(tr_lss, tr_acc))
            print('Validation Set  --- loss:{0}; acc:{1}'.format(vl_lss, vl_acc))

        optimizer.zero_grad()  # zera os gradientes do otimizador
        train_loss.backward()  # faz a passagem de volta
        optimizer.step()  # atualiza os parametros

    # Salva o modelo em disco:
    torch.save(network, MODEL_PATH)
