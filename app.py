import streamlit as st

# Função para calcular a probabilidade de vitória do mandante
def calcular_probabilidade(elo_mandante, elo_visitante):
    prob = (elo_mandante / 400) / ((elo_mandante / 400) + (elo_visitante / 400))
    return prob

# Título da aplicação
st.title("Cálculo de Probabilidade de Vitória - ELO Rating")

# Inputs do usuário
elo_mandante = st.number_input("Informe o ELO do Mandante", min_value=0, value=1500, step=10)
elo_visitante = st.number_input("Informe o ELO do Visitante", min_value=0, value=1500, step=10)

# Botão para calcular a probabilidade
if st.button("Calcular Probabilidade"):
    probabilidade = calcular_probabilidade(elo_mandante, elo_visitante) * 100
    st.write(f"Probabilidade de vitória do Mandante: {probabilidade:.2f}%")
