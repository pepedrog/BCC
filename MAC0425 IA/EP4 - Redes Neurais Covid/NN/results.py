import pandas as pd
import matplotlib.pyplot as plt

import numpy as np

def save_results(results):
    """ Grava os 3 DataFrames como .csv e calcula a média e dp deles """
    results[0].to_csv('../REL/results/results_all.csv')
    results[1].to_csv('../REL/results/results_pcr.csv')
    results[2].to_csv('../REL/results/results_igg.csv')
    results[3].to_csv('../REL/results/results_igm.csv')
    
    df1 = results[0][['acc pcr', 'acc igg', 'acc igm']]
    df2 = results[1]
    df2.insert(0, 'acc igg', results[2]['acc'])
    df2.insert(0, 'acc igm', results[3]['acc'])
    df2 = df2[['acc', 'acc igg', 'acc igm']]
    df2.columns = ['acc pcr', 'acc igg', 'acc igm']
    
    
    data = (df1, df2)
    dfs = []
    for d in data:
        mean = d.mean()
        dv = d.mad()
        worst = d.min()
        best = d.max()
        
        df = pd.DataFrame([mean, dv, worst, best]).transpose()
        df.columns = ['média', 'desvio padrão', 'mínimo', 'máximo']
        dfs.append(df)
        
    dfs[0].to_csv('../REL/results/report_grouped.csv')
    dfs[1].to_csv('../REL/results/report_unique.csv')
    
    plot_result(df1, dfs[0], '../REL/imgs/report_grouped.png')
    plot_result(df2, dfs[1],  '../REL/imgs/report_unique.png')

def plot_result(df, report, path):
    fig, ax = plt.subplots(1, 1)
    ax.boxplot(df.transpose(), labels = df.columns)
    fig.savefig(path)

if __name__ == '__main__':
    results = [pd.read_csv('../REL/results/results_all.csv'),
               pd.read_csv('../REL/results/results_pcr.csv'),
               pd.read_csv('../REL/results/results_igm.csv'),
               pd.read_csv('../REL/results/results_igg.csv')
        ]
    save_results(results)
    