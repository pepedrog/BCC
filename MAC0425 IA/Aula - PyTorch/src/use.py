'''
Programa implementa funcoes para o uso do modelo definido em model.py,
quando ja treinado, para a realizacao de previsoes de chuva,
dadas as features meteorologicas selecionadas em data.py
'''
import torch


def will_it_rain(network, device, rainfall, humidity, rain_today, pressure):
    """Funcao que faz um uso unico da rede treinada"""
    entry = torch.as_tensor([rainfall, humidity, rain_today, pressure]) \
        .float() \
        .to(device)
    output = network(entry)
    return output.ge(0.5).item()  # Binariza o output da rede


def use_network(model_path='FFN_2HLayers_weather.pt', device='cpu'):
    """Funcao que faz um uso unico da rede neural treinada, de maneira amigavel"""
    network = torch.load(model_path)
    message1 = '==> Entre com os dados meteorologicos necessarios para a previsao...\n'
    message2 = '==> [Formato: rainfall/humidity/rain_today/pressure]\n==> '
    awnser = input(message1+message2).split('/')
    if awnser[0] == 'e':
        return False
    rf = float(awnser[0])
    hm = float(awnser[1])
    rt = float(awnser[2])
    pr = float(awnser[3])
    forecast = will_it_rain(network, device, rf, hm, rt, pr)
    if forecast:
        print('\n==> Ira chover amanha\n')
    else:
        print('\n==> Nao ira chover amanha\n')
    return True


def use_iteratively(model_path='FFN_2HLayers_weather.pt', device='cpu'):
    """Funcao que proporciona um menu de uso iterativo da rede neural treinada"""
    print('==> Modelo neural carregado de '+model_path)
    print("==> (Use 'e' para sair)\n")
    keep_going = True
    while keep_going:
        keep_going = use_network(model_path, device)


if __name__ == "__main__":
    model_path = 'FFN_2HLayers_weather.pt'
    use_iteratively(model_path, 'cpu')
