import streamlit as st
import math as mt
import pandas as pd
# Configuração inicial
st.title("Dreidel Manager")

# Inicializar lista de jogadores no estado da sessão
if "jogadores" not in st.session_state:
    st.session_state.jogadores = {}

# Inicializar saldo acumulado
if "sobra_moedas" not in st.session_state:
    st.session_state.sobra_moedas = 0

# Regras do Dreidel
regras = {
    "נ": "Nun - Nada acontece",
    "ג": "Gimel - Pegue tudo",
    "ה": "Hei - Pegue metade",
    "ש": "Shin - Adicione uma moeda"
}

# Gerenciamento de jogadores
st.sidebar.header("Gerenciamento de Jogadores")
nome = st.sidebar.text_input("Nome do jogador")
moedas = st.sidebar.number_input("Moedas iniciais", min_value=1, step=1)

if st.sidebar.button("Adicionar jogador"):
    if nome and nome not in st.session_state.jogadores:
        st.session_state.jogadores[nome] = moedas
        st.sidebar.success(f"Jogador {nome} adicionado com {moedas} moedas!")
    elif nome in st.session_state.jogadores:
        st.sidebar.warning("Jogador já existe!")
    else:
        st.sidebar.error("Insira um nome válido!")

# Opção para excluir jogadores
st.sidebar.header("Excluir Jogador")
if st.session_state.jogadores:
    jogador_para_remover = st.sidebar.selectbox("Selecione um jogador para remover", list(st.session_state.jogadores.keys()))
    if st.sidebar.button("Remover jogador"):
        del st.session_state.jogadores[jogador_para_remover]
        st.sidebar.success(f"Jogador {jogador_para_remover} removido!")
else:
    st.sidebar.write("Nenhum jogador para remover.")

# Mostrar jogadores e saldos
st.header("Jogadores")
if st.session_state.jogadores:
    for jogador, saldo in st.session_state.jogadores.items():
        st.write(f"{jogador}: {saldo} moedas")
else:
    st.write("Nenhum jogador cadastrado.")

# Rodada do Dreidel
st.header("Resultados da Rodada")

# Quantidade de moedas por jogador
moedas_por_jogador = st.number_input("Quantidade de moedas por jogador nesta jogada", min_value=1, step=1)
total_jogadores = len(st.session_state.jogadores)
moedas_em_jogo = (moedas_por_jogador * total_jogadores) + st.session_state.sobra_moedas
st.write(f"Total de moedas em jogo: {moedas_em_jogo} (Quantidade por jogador x Número de jogadores + Sobra de rodadas anteriores)")

# Múltipla escolha para cada jogador
resultados = {}
for jogador in st.session_state.jogadores.keys():
    resultado = st.selectbox(f"Resultado para {jogador}", list(regras.keys()), key=f"resultado_{jogador}")
    resultados[jogador] = resultado

if st.button("Aplicar Resultados"):
    jogadores_para_remover = []  # Lista de jogadores a remover
    ganhadores_gimel = []
    ganhadores_hei = []
    moedas_sobra = moedas_em_jogo

    # Subtrair moedas e processar resultados
    for jogador, resultado in resultados.items():
        # Subtrair as moedas apostadas
        st.session_state.jogadores[jogador] -= moedas_por_jogador
        if resultado == "ג":  # Gimel
            ganhadores_gimel.append(jogador)
        elif resultado == "ה":  # Hei
            ganhadores_hei.append(jogador)
        elif resultado == "ש":  # Shin
            st.session_state.jogadores[jogador] -= 1
            moedas_sobra += 1  # Shin adiciona moeda ao total


    # Distribuir moedas entre ganhadores

    if ganhadores_gimel:
        resto = moedas_sobra % len(ganhadores_gimel) 
        premio = (moedas_sobra - resto) // len(ganhadores_gimel)
        for jogador in ganhadores_gimel:
            st.session_state.jogadores[ganhadores_gimel[0]] += premio
            moedas_sobra = resto
    elif ganhadores_hei:
        if len(ganhadores_hei) == 1:
            premio = moedas_sobra // 2
            sobra = moedas_sobra % 2
            st.session_state.jogadores[ganhadores_hei[0]] += premio
            moedas_sobra = moedas_sobra // 2
        else:
            sobra = moedas_sobra  % len(ganhadores_hei)
            premio = (moedas_sobra - sobra) 
            dividido = premio // len(ganhadores_hei)
            
            for jogador in ganhadores_hei:
                st.session_state.jogadores[jogador] += dividido
            moedas_sobra = sobra
        
    for jogador, resultado in resultados.items():
        if st.session_state.jogadores[jogador] <= 0:
            jogadores_para_remover.append(jogador)


    # Acumular sobras de moedas para a próxima rodada
    st.session_state.sobra_moedas = moedas_sobra
    st.write(f"Sobra de moedas acumuladas para a próxima rodada: {st.session_state.sobra_moedas}")

    # Remover jogadores sem saldo
    for jogador in jogadores_para_remover:
        st.error(f"Jogador {jogador} Eliminado!")
        del st.session_state.jogadores[jogador]

    st.success("Resultados aplicados com sucesso!")