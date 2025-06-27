import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Define o formato da funcao do OHA
def modelo_oscilacao(t, A, b, omega, phi):
    return A * np.exp(-b * t) * np.cos(omega * t - phi)

# Passa os dados da tabela para um vetor
dados = pd.read_csv("posicoes_massa.csv")
df = pd.DataFrame(dados)

df["Posicao X"] -= (np.max(df["Posicao X"]) + np.min(df["Posicao X"])) / 2 
df["Posicao X"] *= 2 / ((np.max(df["Posicao X"]) - np.min(df["Posicao X"])))
df["Posicao X"] *= (58.4/2)/100

t = df['Tempo (s)'].values
x = df['Posicao X'].values

# Ajuste do modelo aos dados
params_iniciais = [1, 1, 20, 0]  # Chutes iniciais para [A, b, omega, phi]
params_otimos, covariancia = curve_fit(modelo_oscilacao, t, x, p0=params_iniciais, maxfev=50000)

# Parâmetros ajustados aos dados
A_ajustado, b_ajustado, omega_ajustado, phi_ajustado = params_otimos

# Gera a curva ajustada
t_ajuste = np.linspace(min(t), max(t), 500)
x_ajuste = modelo_oscilacao(t_ajuste, A_ajustado, b_ajustado, omega_ajustado, phi_ajustado)

# Plota os dados experimentais e da curva ajustada
plt.figure(figsize=(12, 6))
plt.scatter(t, x, color='black', label='Dados experimentais', s=10)
plt.plot(t_ajuste, x_ajuste, 'b-', label=f'Ajuste: $A e^{{-bt}} \cos(\omega t - \phi)$')
plt.title('Posição X da Massa vs. Tempo - Ajuste por Oscilação Harmônica Amortecida', fontsize=14)
plt.xlabel('Tempo (s)', fontsize=12)
plt.ylabel('Posição X (pixels)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

#Calcula o periodo e o fator de qualidade
T = (2*np.pi) / omega_ajustado
fator_qualidade = 2*np.pi / (1 - np.exp(-2*b_ajustado*T))

# Exibe os parâmetros ajustados
texto_ajuste = f'Parâmetros ajustados:\n$A = {A_ajustado:.2f}$\n$b = {b_ajustado:.2f}$\n$\omega = {omega_ajustado:.2f}$\n$\phi = {phi_ajustado:.2f}$\n$FatordeQualidade = {fator_qualidade:.2f}$'
plt.annotate(texto_ajuste, xy=(0.02, 0.7), xycoords='axes fraction', 
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()
plt.show()
