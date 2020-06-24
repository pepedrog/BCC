'''Modulo que realiza testes unitarios nas diferentes componentes que 
constituem o codigo, usando o pacote unittest'''
import unittest
import torch
import numpy as np
from data import load_data, pre_processing
from train import calculate_accuracy, round_tensor, split_data
from use import will_it_rain


class TestData(unittest.TestCase):
    '''Testa as funcoes do modulo data.py, com excessao da funcao de visualizacao'''
    def test_input_data(self):
        '''Testa se os dados carregados do disco sao os esperados'''
        raw_data = load_data()
        self.assertEqual(raw_data.shape[0], 142193)
        self.assertEqual(raw_data.shape[1], 24)

    def test_pre_processing(self):
        '''Testa se as tarefas realizadas no pre-proccessamento estao
        funcionando como deveriam'''
        raw_data = load_data()
        pp_data = pre_processing(raw_data)
        for entry in pp_data['RainToday']:
            self.assertIn(entry, [0, 1])
        for entry in pp_data['RainTomorrow']:
            self.assertIn(entry, [0, 1])
        cols = ['Rainfall', 'Humidity3pm', 'Pressure9am',
                'RainToday', 'RainTomorrow']
        for col in cols:
            for value in pp_data[col]:
                self.assertIsNotNone(value)


class TestTrain(unittest.TestCase):
    '''Testa as funcoes auxiliares do modulo train.py, com excessao da
    funcao de transferencia de dispositivo'''
    def test_accuracy(self):
        '''Testa o calculo da acuracia'''
        gold = np.array([1, 0, 0, 1, 1])
        gold = torch.from_numpy(gold).float()
        prevs = [[1, 0, 0, 1, 1], [0, 1, 1, 0, 0], [1, 1, 0, 0, 1],
                 [1, 1, 1, 0, 1]]
        expected = [1.0, 0.0, 3.0/5.0, 2.0/5.0]
        for i in range(len(prevs)):
            prev = torch.from_numpy(np.array(prevs[i])).float()
            acc = calculate_accuracy(gold, prev)
            self.assertAlmostEqual(acc.item(), expected[i], places=5)

    def test_round(self):
        '''Testa o arredondamento de tensores'''
        tensor = torch.from_numpy(np.array([1.545345])).float()
        resp = round_tensor(tensor)
        self.assertAlmostEqual(resp, 1.545)

        tensor = torch.from_numpy(np.array([23.50900121])).float()
        resp = round_tensor(tensor)
        self.assertAlmostEqual(resp, 23.509)

        tensor = torch.from_numpy(np.array([0.8769615])).float()
        resp = round_tensor(tensor)
        self.assertAlmostEqual(resp, 0.877)

    def test_split(self):
        '''Testa a separacao dos dados em conjuntos de validacao e treinamento'''
        raw_data = load_data()
        pp_data = pre_processing(raw_data)
        (x_tr, y_tr, x_vl, y_vl) = split_data(pp_data)

        self.assertIsNotNone(x_tr)
        self.assertIsNotNone(x_vl)
        self.assertIsNotNone(y_tr)
        self.assertIsNotNone(y_vl)

        ratio_x = len(x_vl) / (len(x_vl) + len(x_tr))
        ratio_y = len(y_vl) / (len(y_vl) + len(y_tr))
        self.assertAlmostEqual(ratio_x, 0.2, places=1)
        self.assertAlmostEqual(ratio_y, 0.2, places=1)


class TestUse(unittest.TestCase):
    '''Classe que testa a funcao will_it_rain, funcao base do modulo use.py.
    Ao avaliar essa funcao, avalia-se tambem se o modelo foi treinado como
    esperado, portanto testa-se indiretamente a funcao principal de
    treinamento e o modulo model.py.'''
    def test_use(self):
        '''Para que esse teste seja realizado, o modelo ja deve ter sido
        treinado.'''
        testing = True
        try:
            model_path = 'FFN_2HLayers_weather.pt'
            network = torch.load(model_path)
        except FileNotFoundError:
            print("Arquivo do modelo nao encontrado. test_use nao realizado. "
                  "Execute o treinamento para que este teste seja rodado")
            testing = False
        if(testing):
            r1 = will_it_rain(network, 'cpu', 10.0, 10.0, 1.0, 2.0)
            r2 = will_it_rain(network, 'cpu', 0.0, 1.0, 0.0, 100.0)
            self.assertEqual(r1, True)
            self.assertEqual(r2, False)


if __name__ == '__main__':
    unittest.main()
