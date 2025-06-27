import pandas as pd
import matplotlib.pyplot as plt

# Supondo que a tabela de dados já foi gerada (como DataFrame do pandas)
# Caso não tenha sido, você pode carregar de um arquivo CSV (descomente a linha abaixo)
# df = pd.read_csv('posicoes_massa.csv')

# Exemplo de DataFrame (simulando os dados coletados)
# (Substitua isso pelos seus dados reais)
dados = pd.read_csv("posicoes_massa.csv")
df = pd.DataFrame(dados)

# Criando o gráfico
plt.figure(figsize=(10, 6))  # Tamanho da figura
plt.plot(df['Tempo (s)'], df['Posicao Y'], 
         marker='o', linestyle='-', color='b', label='Posição Y')

# Adicionando título e rótulos
plt.title('Posição Y da Massa em Função do Tempo', fontsize=14)
plt.xlabel('Tempo (s)', fontsize=12)
plt.ylabel('Posição Y (pixels)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

# Mostrando o gráfico
plt.tight_layout()  # Ajusta o layout para evitar cortes
plt.show()

# Opcional: Salvar o gráfico em um arquivo (descomente a linha abaixo)
# plt.savefig('grafico_posicao_x_vs_tempo.png', dpi=300)