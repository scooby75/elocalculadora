import streamlit as st

# Função para calcular a probabilidade ajustada pelo ELO, xG, performance recente e H2H
def calcular_probabilidade_ajustada(elo_mandante, elo_visitante, xg_mandante, xg_visitante, 
                                    perf_ultimos_jogos, perf_h2h):
    # Calcular a probabilidade baseada no ELO (com intervalo ajustado para 0 a 100)
    prob_elo = (elo_mandante / 100) / ((elo_mandante / 100) + (elo_visitante / 100))

    # Ajuste com base nos valores de xG (ponderando com 20% do peso de xG)
    ajuste_xg = ((xg_mandante - xg_visitante) * 0.2)
    
    # Ajuste com base na performance dos últimos 5 jogos (ponderando com 15% do peso)
    ajuste_perf_jogos = (perf_ultimos_jogos - 50) * 0.15 / 100
    
    # Ajuste com base no histórico H2H (ponderando com 10% do peso)
    ajuste_h2h = (perf_h2h - 50) * 0.10 / 100
    
    # Probabilidade final com todos os ajustes
    prob_final = prob_elo + ajuste_xg + ajuste_perf_jogos + ajuste_h2h
    return max(0, min(prob_final, 1))  # Garantir que o valor esteja entre 0 e 1

# Função para calcular a linha de handicap asiático com base na probabilidade
def calcular_handicap_asiatico(probabilidade):
    if probabilidade >= 75:
        return -1.5  # Linha forte de HA
    elif 65 <= probabilidade < 75:
        return -1.0  # Favorito claro
    elif 55 <= probabilidade < 65:
        return -0.75  # Leve favorito
    elif 45 <= probabilidade < 55:
        return -0.5  # Quase equilibrado
    elif 35 <= probabilidade < 45:
        return 0  # Empate anula aposta
    else:
        return +0.5  # Time visitante ligeiramente favorito

# Título da aplicação
st.title("Cálculo de Probabilidade")

# Inputs do usuário para ELO
elo_mandante = st.number_input("Informe o ELO do Mandante (0 a 100)", min_value=0, max_value=100, value=50, step=1)
elo_visitante = st.number_input("Informe o ELO do Visitante (0 a 100)", min_value=0, max_value=100, value=50, step=1)

# Inputs do usuário para xG
xg_mandante = st.number_input("Informe o xG do Mandante", min_value=0.0, value=1.5, step=0.1)
xg_visitante = st.number_input("Informe o xG do Visitante", min_value=0.0, value=1.2, step=0.1)

# Inputs para a performance dos últimos 5 jogos em casa do mandante (em % de vitórias)
perf_ultimos_jogos = st.number_input("Informe a performance dos últimos 5 jogos em casa do Mandante (0 a 100%)", 
                                     min_value=0.0, max_value=100.0, value=50.0, step=1.0)

# Inputs para a performance dos últimos 5 confrontos H2H (em % de vitórias do Mandante)
perf_h2h = st.number_input("Informe a performance dos últimos 5 confrontos H2H do Mandante (0 a 100%)", 
                           min_value=0.0, max_value=100.0, value=50.0, step=1.0)

# Botão para calcular a probabilidade ajustada, odd e handicap asiático
if st.button("Calcular"):
    probabilidade = calcular_probabilidade_ajustada(elo_mandante, elo_visitante, xg_mandante, xg_visitante, 
                                                    perf_ultimos_jogos, perf_h2h) * 100
    odd = 100 / probabilidade if probabilidade > 0 else float('inf')  # Evitar divisão por zero
    
    # Calcular a linha de handicap asiático com base na probabilidade
    handicap_asiatico = calcular_handicap_asiatico(probabilidade)

    # Exibir resultados
    st.write(f"Probabilidade: {probabilidade:.2f}%")
    st.write(f"Odd Justa: {odd:.2f}")
    st.write(f"Linha HA: {handicap_asiatico}")
