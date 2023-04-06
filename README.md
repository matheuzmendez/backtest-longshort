# Backtest - LongShort

Este código realiza um backtest de uma estratégia de investimento para a ação PETR4.SAO utilizando a API da Alpha Vantage. A estratégia consiste em entrar short (vender) no leilão de fechamento caso o preço da ação tenha subido mais de 1% no dia anterior e sair da posição caso o preço atinja uma queda de 2% (stop loss) ou suba 1% (stop gain) em relação ao preço de entrada.

O código faz uma série de requisições à API para obter os dados históricos de preços da ação e processa os dados para criar as colunas necessárias para a estratégia. Em seguida, é realizado um loop para percorrer os dias do histórico, aplicar a estratégia e calcular o resultado do backtest.

O resultado é plotado em um gráfico de linha com o retorno acumulado da estratégia. Além disso, foi adicionado um benchmark com o Ibovespa para melhor visualização do desempenho.
