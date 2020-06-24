"""
Script principal, que chama as funcoes dos outros modulos para
carregar os dados, fazer o pre-processmanto e adequacao, instanciar
uma rede neural Feed-Foward com 2 camadas ocutas e treina-la, utilizando
os dados processados para prever se chovera amanha,
dados os valores de features meteorologicas selecionadas.
Salva tambem o modelo em disco e abre um menu iterativo para a utilizacao
exploratoria do  modelo.
"""


from data import load_data, pre_processing, visualize_data
from use import use_iteratively
from model import FFN_2HLayers
from train import split_data, train_network
import torch


N_HL1 = 5
N_HL2 = 3
LEARNING_RATE = 0.001
MODEL_PATH = 'FFN_2HLayers_weather.pt'


if __name__ == "__main__":
    print('CARREGANDO DADOS...')
    raw_data = load_data()

    print('PRE-PROCESSANDO DADOS...')
    processed_data = pre_processing(raw_data)

    print('GERANDO VISUAIZACOES DOS DADOS...')
    visualize_data(processed_data)

    print('ADEQUANDO DADOS PARA TREINAMENTO...')
    splitted_data = split_data(processed_data)

    print('MONTANDO MODELO...')
    x_train = splitted_data[0]
    network = FFN_2HLayers(x_train.shape[1], N_HL1, N_HL2)
    optimizer = torch.optim.Adam(network.parameters(), lr=LEARNING_RATE)
    criterion = torch.nn.BCELoss()

    print('TREINANDO...')
    train_network(splitted_data, network, optimizer, criterion, MODEL_PATH)
    print('MODELO TREINADO. (Salvo em ' + MODEL_PATH + ')')

    # Uso iterativo do modelo:
    print('Use o menu a seguir para explorar o modelo iterativamente:\n')
    use_iteratively()

    print('FIM.')
