import streamlit as st

# Função para calcular a probabilidade ajustada pelo ELO e xG
def calcular_probabilidade_ajustada(elo_mandante, elo_visitante, xg_mandante, xg_visitante):
    # Calcular a probabilidade baseada no ELO
    prob_elo = (elo_mandante / 400) / ((elo_mandante / 400) + (elo_visitante / 400))

    # Ajuste com base nos valores de xG (ponderando com 20% do peso de xG)
    ajuste_xg = ((xg_mandante - xg_visitante) * 0.2)
    
    # Probabilidade final com ajuste de xG
    prob_final = prob_elo + ajuste_xg
    return max(0, min(prob_final, 1))  # Garantir que o valor esteja entre 0 e 1

# Título da aplicação
st.title("Cálculo de Probabilidade de Vitória - ELO + xG")

# Inputs do usuário para ELO
elo_mandante = st.number_input("Informe o ELO do Mandante", min_value=0, value=1500, step=10)
elo_visitante = st.number_input("Informe o ELO do Visitante", min_value=0, value=1500, step=10)

# Inputs do usuário para xG
xg_mandante = st.number_input("Informe o xG do Mandante", min_value=0.0, value=1.5, step=0.1)
xg_visitante = st.number_input("Informe o xG do Visitante", min_value=0.0, value=1.2, step=0.1)

# Botão para calcular a probabilidade ajustada e a odd
if st.button("Calcular Probabilidade e Odd"):
    probabilidade = calcular_probabilidade_ajustada(elo_mandante, elo_visitante, xg_mandante, xg_visitante) * 100
    odd = 100 / probabilidade if probabilidade > 0 else float('inf')  # Evitar divisão por zero

    # Exibir resultados
    st.write(f"Probabilidade ajustada de vitória do Mandante: {probabilidade:.2f}%")
    st.write(f"Odd calculada: {odd:.2f}")
