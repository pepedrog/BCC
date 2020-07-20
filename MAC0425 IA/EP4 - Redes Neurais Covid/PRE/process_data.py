"""
Script de tratamento dos dados

Aqui estão as funções responsáveis pelo carregamento dos dados e 
tratamento dos DataFrames obtidos para padronização de execução na rede neural

As funções principais são

- load_data():  
    Carrega os arquivos puros da pasta ./dados_raw/
    E retorna um DataFrame de pacientes e outro de exames
                
- process_data(pacientes, exames): 
    Faz um tratamento intenso dos DataFrames
    Limpa os dados, une os pacientes com exames,
    escolhe quais exames serão usados e
    agrupa os exames por paciente e data de coleta.
    
    Escreve dados intermediários na pasta ./dados_inter/
    Escreve os dados processados na pasta ./dados_final/
    E retorna os DatatFrames equivalentes
 
"""

import pandas as pd
import numpy as np

def load_data():
    """ Importa dados dos arquivos .csv usando pandas  """
    p = pd.read_csv('./dados_raw/einstein_p.csv', 
                    sep = '|',
                    usecols = [0, 1, 2],
                    names = ['id_paciente', 'sexo', 'nascimento'],
                    header = 0)
    
    e = pd.read_csv('./dados_raw/einstein_e.csv', 
                    sep = '|',  
                    usecols = [0, 1, 4, 5], 
                    names = ['id_paciente', 'data_coleta', 'analito', 'resultado'],
                    header = 0)
    return p, e

def count_exames(exames):
    """ Conta todas as intâncias de tipos de exames diferentes """
    count = exames[['analito', 'id_paciente']]
    count = count.groupby(['analito'])['id_paciente'] \
                          .count().reset_index(name='count') \
                          .sort_values(['count'], ascending=False)
    return count

def process_analitos(exames, count):
    """ Trabalho manual de limpeza dos dados e tomada de decisões """
    
    # Vamos considerar apenas o resultado de Igg e Igm, sem considerar o valor numérico
    exames = exames[exames['analito'] != 'IgG, COVID19']
    exames = exames[exames['analito'] != 'IgM, COVID19']
    
    # Vamos considerar o teste rápido junto com os outros testes
    exames.loc[exames['analito'] == 'COVID19 IgM, teste rápido', 'analito'] = 'COVID IgM Interp'
    exames.loc[exames['analito'] == 'COVID19 IgG, teste rápido', 'analito'] = 'COVID IgG Interp'
    
    # Existem ~poucos exames de IgG e IgM nos dados, 
    # então vamos considerar todos os exames com mais instâncias que esses
    quant_igg = count.loc[count['analito'] == 'COVID IgM Interp', 'count'].item()
    quant_igm = count.loc[count['analito'] == 'COVID IgG Interp', 'count'].item()
    lim_exames = min(quant_igg, quant_igm)
    
    features = count.loc[count['count'] >= lim_exames, 'analito'].to_list()

    # Filtro apenas os exames features
    exames = exames.loc[exames['analito'].isin(features)]
    
    return exames, features

def process_resultados(exames):
    """ Trabalho manual de limpeza dos resultados dos exames """
    
    # Normalizar todos os booleanos para 0 e 1
    exames.loc[exames['resultado'] == 'Reagente', 'resultado'] = 1
    exames.loc[exames['resultado'] == 'Detectado', 'resultado'] = 1
    exames.loc[exames['resultado'] == 'Presente', 'resultado'] = 1
    exames.loc[exames['resultado'] == 'Positivo', 'resultado'] = 1
    exames.loc[exames['resultado'] == 'Reagente Fraco', 'resultado'] = 0
    exames.loc[exames['resultado'] == 'Não Reagente', 'resultado'] = 0
    exames.loc[exames['resultado'] == 'Não reagente', 'resultado'] = 0
    exames.loc[exames['resultado'] == 'Não Detectado', 'resultado'] = 0
    exames.loc[exames['resultado'] == 'Não detectado', 'resultado'] = 0
    exames.loc[exames['resultado'] == 'Negativo', 'resultado'] = 0
    exames.loc[exames['resultado'] == 'Ausentes', 'resultado'] = 0
    exames.loc[exames['resultado'] == 'Ausente', 'resultado'] = 0
    
    # Arruma os exames para resultados numéricos
    exames.replace(to_replace = ',', value = '.', inplace = True, regex = True)
    exames.replace(to_replace = ' [Ll](itro)*(s)*', value = '', inplace = True, regex = True)
    exames.replace(to_replace = '[><%]', value = '', inplace = True, regex = True)

    # Deleta todos os resultados nulos ou não numéricos (cerca de 0,2%)
    is_null = pd.to_numeric(exames['resultado'], errors='coerce')
    idx = is_null.isna()
    exames = exames[~idx]
    
    return exames

def group_exames(exames, features):
    """ Monta o DF que será usado de input para a rede 
        Agrupando os exames-features por paciente e data """
    
    cols = ['nascimento', 'sexo']
    cols.extend(features)
    
    df = pd.DataFrame([], columns = cols)
    
    # As instâncias estarão associadas ao par (paciente, data)
    exames.drop_duplicates(['id_paciente', 'data_coleta', 'analito'], inplace = True)
    instances = exames.groupby(['id_paciente', 'data_coleta'])
    
    rows_pcr = [df]
    rows_igg = [df]
    rows_igm = [df]
    rows_all = [df]
    
    for _, group in instances:

        pcr = igg = igm = False
        row = group.drop(columns = ['id_paciente', 'data_coleta', 'sexo', 'nascimento'])
        row = row.transpose()
        
        row.columns = row.loc['analito']
        if len(row.columns) < 15: continue
        
        row.drop('analito', inplace = True)
        
        row.insert(0, 'sexo', group['sexo'].iloc[0])
        row.insert(0, 'nascimento', group['nascimento'].iloc[0])
        
        if 'Resultado COVID-19:' in row.columns:
            pcr = True
            rows_pcr.append(row)
        if 'COVID IgG Interp' in row.columns:
            igg = True
            rows_igg.append(row)
        if 'COVID IgM Interp' in row.columns:
            igm = True
            rows_igm.append(row)
        if pcr and igg and igm:
            rows_all.append(row)
    
    df_pcr = pd.concat(rows_pcr)
    df_igg = pd.concat(rows_igg)
    df_igm = pd.concat(rows_igm)
    df_all = pd.concat(rows_all)
    
    df_pcr.to_csv('./dados_inter/einstein_grouped_pcr.csv')
    df_igg.to_csv('./dados_inter/einstein_grouped_igg.csv')
    df_igm.to_csv('./dados_inter/einstein_grouped_igm.csv')
    df_all.to_csv('./dados_inter/einstein_grouped_all.csv')
    
    return df_pcr, df_igg, df_igm, df_all

def final_clean(exames):
    """ Elimina os exames com poucos resultados """
    total = len(exames.index)
    to_drop = []
    for c in exames.columns:
         if exames[c].count() < total/2:
             to_drop.append(c)
             
    return exames.drop(columns = to_drop)

def fill_empty(exames):
    """ Preenche todos os exames sem resultado com o valor de referência """
    ref = {'Hematócrito' : 40,
           'Hemoglobina' : 13,
           'Plaquetas' : 340,
           'Hemácias' : 4,
           'Leucócitos' : 6,
           'Leucócitos #' : 6000,
           'VCM' : 90,
           'CHCM' : 34,
           'HCM' : 30,
           'Linfócitos #' : 2000,
           'Monócitos #' : 400,
           'Linfócitos' : 20,
           'Monócitos' : 9,
           'RDW' : 13,
           'Eosinófilos  #' : 250,
           'Eosinófilos' : 3,
           'Basófilos #' : 50,
           'Basófilos' : 0.5,
           'Volume Médio Plaquetário' : 10,
           'Potássio' : 4,
           'Creatinina' : 0.7,
           'Sódio' : 140,
           'Uréia' : 25,
           'Neutrófilos' : 50,
           'Neutrófilos  #' : 5000,
           'TGP' : 20,
           'TGO' : 30,
          }
    return exames.fillna(value = ref)

# ---------- Função principal de processamento ----------
def process_data(pacientes, exames):
    """ Limpa todo o dataframe e padroniza os dados """
    
    # Processa os pacientes
    pacientes.drop_duplicates(['id_paciente'], inplace = True)
    pacientes.loc[pacientes['nascimento'] == 'AAAA', 'nascimento'] = '1930'
    pacientes['sexo'] = pacientes['sexo'].map({'M': 0, 'F': 1})
    
    # Processa os exames
    exames.drop_duplicates(inplace = True)
    
    count = count_exames(exames)
    
    exames, features = process_analitos(exames, count)
    
    exames = process_resultados(exames)
    
    exames = exames.merge(pacientes, on = 'id_paciente', how = 'left')
    
    count.to_csv('./dados_inter/einstein_e_count.csv')
    
    dfs = group_exames(exames, features)
    
    # Dropa as colunas dos outros exames no df do exame específico
    dfs[0].drop(columns = ['COVID IgG Interp', 'COVID IgM Interp'], inplace = True)
    dfs[1].drop(columns = ['Resultado COVID-19:', 'COVID IgM Interp'], inplace = True)
    dfs[2].drop(columns = ['Resultado COVID-19:', 'COVID IgG Interp'], inplace = True)
      
    final = []
    for d in dfs:
        d = final_clean(d)
        d = fill_empty(d)
        final.append(d)
    
    final[0].to_csv('./dados_final/einstein_processed_pcr.csv', index = False)
    final[1].to_csv('./dados_final/einstein_processed_igg.csv', index = False)
    final[2].to_csv('./dados_final/einstein_processed_igm.csv', index = False)
    final[3].to_csv('./dados_final/einstein_processed_all.csv', index = False)
    
    return final

if __name__ == "__main__":
    print('LOADING DATA ...')
    p, e = load_data()
    print('PROCESSING DATA (might take some minutes) ...')
    exames = process_data(p, e)