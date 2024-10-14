import streamlit as st

# Função para calcular a probabilidade ajustada pelo ELO e xG
def calcular_probabilidade_ajustada(elo_mandante, elo_visitante, xg_mandante, xg_visitante):
    # Calcular a probabilidade baseada no ELO (com intervalo ajustado para 0 a 100)
    prob_elo = (elo_mandante / 100) / ((elo_mandante / 100) + (elo_visitante / 100))

    # Ajuste com base nos valores de xG (ponderando com 20% do peso de xG)
    ajuste_xg = ((xg_mandante - xg_visitante) * 0.2)
    
    # Probabilidade final com ajuste de xG
    prob_final = prob_elo + ajuste_xg
    return max(0, min(prob_final, 1))  # Garantir que o valor esteja entre 0 e 1

# Função para estimar linha de handicap asiático com base na probabilidade ajustada
def estimar_handicap_asiatico(probabilidade):
    if probabilidade < 40:
        return "+1.0 ou superior"
    elif 40 <= probabilidade <= 60:
        return "0.0 (Pick’em)"
    else:
        return "-1.0 ou superior"

# Título da aplicação
st.title("Cálculo de Probabilidade de Vitória e Linha de Handicap Asiático")

# Inputs do usuário para ELO
elo_mandante = st.number_input("Informe o ELO do Mandante (0 a 100)", min_value=0, max_value=100, value=50, step=1)
elo_visitante = st.number_input("Informe o ELO do Visitante (0 a 100)", min_value=0, max_value=100, value=50, step=1)

# Inputs do usuário para xG
xg_mandante = st.number_input("Informe o xG do Mandante", min_value=0.0, value=1.5, step=0.1)
xg_visitante = st.number_input("Informe o xG do Visitante", min_value=0.0, value=1.2, step=0.1)

# Botão para calcular a probabilidade ajustada, a odd e a linha de handicap asiático
if st.button("Calcular Probabilidade, Odd e Linha de Handicap"):
    probabilidade = calcular_probabilidade_ajustada(elo_mandante, elo_visitante, xg_mandante, xg_visitante) * 100
    odd = 100 / probabilidade if probabilidade > 0 else float('inf')  # Evitar divisão por zero
    linha_handicap = estimar_handicap_asiatico(probabilidade)

    # Exibir resultados
    st.write(f"Probabilidade ajustada de vitória do Mandante: {probabilidade:.2f}%")
    st.write(f"Odd calculada: {odd:.2f}")
    st.write(f"Linha de Handicap Asiático estimada: {linha_handicap}")
