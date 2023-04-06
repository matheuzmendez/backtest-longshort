import requests
import pandas as pd
import time
import matplotlib.pyplot as plt

api_key = "KBO4M3U3J3OBAITU"

# Fazer a primeira requisição na API Alpha Vantage para obter o número total de dias
response = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=PETR4.SAO&outputsize=full&apikey={api_key}")
total_dias = len(response.json()["Time Series (Daily)"])

# Definir o tamanho da página (máximo 100 dias por chamada)
page_size = 100

# Inicializar o DataFrame vazio
data = pd.DataFrame()
data = data.sort_index(ascending=False)

# Loop para percorrer todas as páginas
for i in range(0, 100, page_size):
    # Fazer a requisição na API Alpha Vantage para obter os dados de preços históricos para ITSA4
    response = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=PETR4.SAO&outputsize=full&apikey={api_key}")
    dados = pd.DataFrame(response.json()["Time Series (Daily)"]).T
    dados.index = pd.to_datetime(dados.index)
    dados = dados.astype(float)
    
    # Concatenar os dados da página atual com o DataFrame geral
    data = pd.concat([data, dados])
    
    # Esperar 15 segundos antes de fazer a próxima requisição (para respeitar o limite da API Alpha Vantage)
    # time.sleep(15)
    
# Definir parâmetros do backtest
porcentagem_subida = 0.01
porcentagem_stop_loss = 0.02
porcentagem_stop_gain = 0.01

# Criar coluna para sinalizar dias com subida acima de 10%
data['subiu_10'] = data['4. close'].pct_change() > porcentagem_subida

# Criar coluna para calcular o retorno diário
data['return'] = data['4. close'].pct_change()

# Criar colunas para guardar posição, stop loss e stop gain
data['posicao'] = 0
data['stop_loss'] = 0
data['stop_gain'] = 0

# Loop para percorrer os dias do histórico
for i in range(1, len(data)):
    # Se o dia anterior subiu mais de 10%, entrar short no leilão de fechamento
    if data.loc[data.index[i-1], 'subiu_10']:
        data.loc[data.index[i], 'posicao'] = -1
    
    # Se estiver com posição aberta, definir stop loss e stop gain
    if data.loc[data.index[i], 'posicao'] != 0:
        preco_entrada = data.loc[data.index[i-1], '4. close']
        data.loc[data.index[i], 'stop_loss'] = preco_entrada * (1 - porcentagem_stop_loss)
        data.loc[data.index[i], 'stop_gain'] = preco_entrada * (1 + porcentagem_stop_gain)
        
        # Verificar se houve execução do stop loss ou stop gain
        if data.loc[data.index[i], '3. low'] <= data.loc[data.index[i], 'stop_loss']:
            data.loc[data.index[i], 'posicao'] = 0
        elif data.loc[data.index[i], '2. high'] >= data.loc[data.index[i], 'stop_gain']:
            data.loc[data.index[i], 'posicao'] = 0

# Calcular resultado do backtest
resultado = (data['posicao'].shift(1) * data['return']).fillna(0)
retorno_acumulado = (1 + resultado).cumprod()

print(resultado)
print(retorno_acumulado)


# Plota os principais gráficos

# Criar gráfico de linha
plt.plot(retorno_acumulado)

# Configurar rótulos e título
plt.xlabel('Data')
plt.ylabel('Retorno Acumulado')
plt.title('Retorno Acumulado do Backtest')

# Exibir gráfico
plt.show()

time.sleep(30)