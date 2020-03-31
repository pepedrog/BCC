import csv

class pessoa:
  """ Classe pessoa

    Possui nome e dois arrays de dicionários,
    cada dicionário possui informação sobre uma corrida.

    Possui um método para devolver a velocidade média da pessoa
    em cada tipo de corrida.
  """
  def __init__(self, nome):
    self.nome = nome
    self.mu_data = []
    self.muv_data = []

  def insert_mu(self, data):
    """
      Wrapper para inserir dados de uma corrida MU.

      Verifica se é uma corrida com cronômetros alternados
      e chama função apropriada
    """
    if "T1a" in data:
      self.insert_mu_aligned(data)
    else:
      self.insert_mu_alternate(data)

  def insert_mu_alternate(self, data):
    """
    Insere dados de uma corrida MU com cronômetros alternados

    Deve retornar um dicionário contendo:
      - Tempo em cada um dos setores
      - Velocidade média
    """
    dct = {}


    dct["cron"] = [0] + \
      [float(data["T%d" % (i)]) for i in range(1,7)] # Dados do cronômetro (acrescido do 0 em x0)
    dct["speed"] = 30/dct["cron"][-1] # Vm = dx/dt
    dct["sector"] = [5*i for i in range(7)] # Posição de cada setor

    # Garantindo compatibilidade p/ análise futura desses dados
    assert(len(dct["cron"]) == len(dct["sector"]))

    # Adiciona dados à lista
    self.mu_data.append(dct)

  def insert_mu_aligned(self, data):
    """
    Insere dados de uma corrida MU com cronômetros alinhados

    Deve retornar um dicionário contendo:
      - Tempo em cada um dos setores
      - Velocidade média
    """
    dct = {} # Cria dicionário a ser retornado

    dct["cron"] = [0] + [ # Dados dos cronômetros
      ( # Utilizamos a média dos crônometros
        float(data["T%da" % (i)]) +
        float(data["T%db" % (i)])
      )/2
      for i in range(1,4)
    ]

    dct["speed"] = 30/dct["cron"][-1] # Vm = dx/dt
    dct["sector"] = [10*i for i in range(4)] # Posição de cada setor

    # Garantindo compatibilidade p/ análise futura desses dados
    assert(len(dct["cron"]) == len(dct["sector"]))

    # Adiciona dados à lista
    self.mu_data.append(dct)

  def process_mu(self):
    # Calcula Velocidade média no MU
    self.mu_speed = \
      (self.mu_data[0]["speed"] + self.mu_data[1]["speed"] + self.mu_data[2]["speed"])/3

    # Calcula o erro médio no MU
    self.mu_err = 0
    spd = self.mu_speed # 'constante' temporária
    for exp in self.mu_data: # Para cada amostragem
      err = 0

      # Para cada setor
      for i in range(1,len(exp["sector"])):
        # Diferença entre posição do setor (real) e a posição esperada
        # Dado o tempo e a velocidade média
        rel = (exp["sector"][i] - exp["cron"][i]*spd)**2
        err += rel

      # Divide o erro em relação a quantidade de setores
      err /= len(exp["sector"])
      err = err**(1/2)

      # Normaliza o erro em relação ao tempo total em %
      err = (err/exp["cron"][-1])*100

      # Soma ao erro total
      self.mu_err += err

    self.mu_err /= 3 # Divide pela quantidade

  def plot_mu(self):
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np

    # Cria figura
    fig, ax = plt.subplots()
    ax.set(xlabel = "Tempo (s)", ylabel = "Posição (m)")
    ax.set(title="MU - %s \n Erro (desvio padrão): %3.3f%%" % (self.nome, self.mu_err))

    # Simulação
    sim_x = np.arange(0, 30, 0.01)
    sim_y = [self.mu_speed*sim_x[i] for i in range(len(sim_x))] # dx = dvdt
    ax.plot(sim_x, sim_y, label="Simulação")

    # Dados
    i = 1
    for data in self.mu_data:
      ax.plot(data["cron"], data["sector"], linestyle=":", linewidth=2, label="Experimento %d" % (i))
      i += 1

    # Salvando gráfico
    ax.legend()
    fig.savefig("%s_MU.png" % (self.nome.lower().replace(" ","")))

  def insert_muv(self, data):
    """
      Wrapper para inserir dados de uma corrida MU

      Verifica se é uma corrida com cronômetros alternados
      e chama função apropriada
    """
    if "T1a" in data:
      self.insert_muv_aligned(data)
    else:
      self.insert_muv_alternate(data)

  def insert_muv_alternate(self, data):
    """
      Insere dados de uma corrida MUV
      com cronômetros alternados

      Deve retornar um dicionário contendo:
      - Tempo em cada um dos setores
      - Velocidade em cada um dos setores
      - Velocidade média
      - Aceleração média
    """
    dct = {}

    dct["cron"] = [0] + \
      [float(data["T%d" % (i)]) for i in range(1,7)] # Dados do cronômetro (acrescido do 0 em x0)
    dct["speed"] = 30/dct["cron"][-1] # Vm = dx/dt
    # Utilizamos o dobro da velocidade média para calcular
    # aceleração pois esta é aproximadamente à velocidade final
    # (image o trapézio do gráfico v(t))
    dct["accel"] = 4*dct["speed"]**2/60 # a = v^2/2dx
    dct["sector"] = [5*i for i in range(7)] # Posição de cada setor
    dct["sector_speed"] = [0] # Velocidade em cada setor
    for i in range(1,len(dct["sector"])):
      dct["sector_speed"].append( # Vm = (x1 - x0)/(t1 - t0)
        (dct["sector"][i] - dct["sector"][i-1])/
        (dct["cron"][i] - dct["cron"][i-1])
      )

    # Adiciona dados à lista
    self.muv_data.append(dct)

  def insert_muv_aligned(self, data):
    """
      Insere dados de uma corrida MUV
      com cronômetros alinhados

      Deve retornar um dicionário contendo:
      - Tempo em cada um dos setores
      - Velocidade em cada um dos setores
      - Velocidade média
      - Aceleração média
    """
    dct = {}

    dct["cron"] = [0] + \
      [
        (
          float(data["T%da" % (i)]) +
          float(data["T%db" % (i)])
        )/2
        for i in range(1,4)
      ] # Dados do cronômetro (acrescido do 0 em x0)
    dct["speed"] = 30/dct["cron"][-1] # Vm = dx/dt
    # Utilizamos o dobro da velocidade média para calcular
    # aceleração pois esta é aproximadamente à velocidade final
    # (image o trapézio do gráfico v(t))
    dct["accel"] = 4*dct["speed"]**2/60 # a = v^2/2dx
    dct["sector"] = [10*i for i in range(4)] # Posição de cada setor
    dct["sector_speed"] = [0] # Velocidade em cada setor
    for i in range(1,len(dct["sector"])):
      dct["sector_speed"].append( # Vm = (x1 - x0)/(t1 - t0)
        (dct["sector"][i] - dct["sector"][i-1])/
        (dct["cron"][i] - dct["cron"][i-1])
      )

    # Adiciona dados à lista
    self.muv_data.append(dct)

  def process_muv(self):
    # Calcula Velocidade média no MUV
    self.muv_speed = \
      (self.muv_data[0]["speed"] + self.muv_data[1]["speed"] + self.muv_data[2]["speed"])/3

    # Calcula Aceleração média no MUV
    self.muv_accel = \
      (self.muv_data[0]["accel"] + self.muv_data[1]["accel"] + self.muv_data[2]["accel"])/3

    # Calcula o erro médio da posição no MUV
    self.muv_err_pos = 0
    accel = self.muv_accel # 'constante' temporária
    for exp in self.muv_data: # Para cada amostragem
      err = 0

      # Para cada setor
      for i in range(1,len(exp["sector"])):
        # Diferença entre posição do setor (real) e a posição esperada
        # Dado o tempo e a aceleração média
        # X = x0 + v0t + at^2/2
        rel = (exp["sector"][i] - ((accel*(exp["cron"][i]**2)/2)))**2
        err += rel

      # Divide o erro em relação a quantidade de setores
      err /= len(exp["sector"])
      err = err**(1/2)

      # Normaliza o erro em relação ao tempo total em %
      err = (err/exp["cron"][-1])*100

      # Soma ao erro total
      self.muv_err_pos += err

    self.muv_err_pos /= 3 # Divide pela quantidade

    # Calcula o erro médio da velocidade no MUV
    self.muv_err_spd = 0
    accel = self.muv_accel # 'constante' temporária
    for exp in self.muv_data:
      err = 0

      # Para cada setor
      for i in range(1,len(exp["sector_speed"])):
        # Diferença entre velocidade do setor (real) e a velocidade
        # esperada dada o tempo e aceleração média
        # v = v0 + at
        rel = (exp["sector_speed"][i] - (accel*exp["cron"][i]))**2
        err += rel

      # Divide o erro em relação à qtd de setores
      err /= len(exp["sector"])
      err = err**(1/2)

      # Normaliza o erro em relação ao tempo total em %
      err = (err/exp["cron"][-1])*100

      # Soma ao erro total
      self.muv_err_spd += err

    self.muv_err_spd /= 3 # Divide pela quantidade

  def plot_muv(self):
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np

    # Gráfico X(t)
    # Cria figura
    fig, ax = plt.subplots()
    ax.set(xlabel = "Tempo (s)", ylabel = "Posição (m)")
    ax.set(title="MUV - %s \n Erro (desvio padrão): %3.3f%%" % (self.nome, self.muv_err_pos))

    # Simulação
    sim_x = np.arange(0, 25, 0.01)
    sim_y = [self.muv_accel*(sim_x[i]**2)/2 for i in range(len(sim_x))] # X = at^2/2
    ax.plot(sim_x, sim_y, label="Simulação")

    # Dados
    i = 1
    for data in self.muv_data:
      ax.plot(data["cron"], data["sector"], linestyle=":", linewidth=2, label="Experimento %d" % (i))
      i += 1

    # Salvando gráfico
    ax.legend()
    fig.savefig("%s_MUV_xt.png" % (self.nome.lower().replace(" ","")))

  def plot_muv2(self):
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np

    # Gráfico v(t)
    # Cria figura
    fig2, ax2 = plt.subplots()
    ax2.set(xlabel = "Tempo (s)", ylabel = "Velocidade (m/s)")
    ax2.set(title="MUV - %s \n Erro (desvio padrão): %3.3f%%" % (self.nome, self.muv_err_spd))

    # Simulação
    sim_x = np.arange(0, 25, 0.01)
    sim_y = [self.muv_accel*sim_x for i in range(len(sim_x))] # dv = adt
    ax2.plot(sim_x, sim_y, label="Simulação")

    # Dados
    i = 1
    for data2 in self.muv_data:
      ax2.plot(data2["cron"], data2["sector_speed"], linestyle=":", linewidth=2, label="Experimento %d" % (i))
      i += 1

    # Salvando gráfico
    ax2.legend()
    fig2.savefig("%s_MUV_vt.png" % (self.nome.lower().replace(" ","")))



# Cria cada uma das pessoas
pessoas = {
  "1": pessoa("Lucas Fujiwara"),
  "2": pessoa("Pedro Gigeck"),
  "4": pessoa("Isis Logullo")
}

# Insere o dicionário de cada corrida
# Arquivos
files = ["mov_unif.csv", "mov_unif_alt.csv", "mov_unif_var.csv", "mov_unif_var_alt.csv"]
for file in files: # Para cada arquivo
  with open(file) as csvfile:
    reader = csv.DictReader(csvfile)
    for line in reader: # Lê uma entrada
      if "var" in file: # Se for MUV, insere como MUV
        pessoas[str(line["ID"][0])].insert_muv(line)
      else: # Se não, insere como MU
        pessoas[str(line["ID"][0])].insert_mu(line)

mean_accel = 0
mean_spd = 0

# Processa o que cada pessoa fez
for x in pessoas.values():
  x.process_muv()
  x.process_mu()
  x.plot_mu()
  x.plot_muv()
  x.plot_muv2()
  mean_accel += x.muv_accel
  mean_spd += x.mu_speed

mean_accel /= 3
mean_spd /= 3

print("Velocidade média: %2.5f" % (mean_spd))
print("Aceleração média: %2.5f" % (mean_accel))