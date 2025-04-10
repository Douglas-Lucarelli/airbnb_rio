import pandas as pd
import streamlit as st
import joblib

st.set_page_config(page_title="Previsão de Preço - Airbnb Rio", layout="centered")

st.title("🏡 Previsão de Preço de Imóvel no Airbnb Rio")

# ========= Funções Auxiliares =========

def coleta_inputs():
    # Entradas numéricas
    x_numericos = {
        'latitude': st.number_input('latitude', step=0.00001, format="%.5f"),
        'longitude': st.number_input('longitude', step=0.00001, format="%.5f"),
        'accommodates': st.number_input('accommodates', step=1, value=1),
        'bathrooms': st.number_input('bathrooms', step=1, value=1),
        'bedrooms': st.number_input('bedrooms', step=1, value=1),
        'beds': st.number_input('beds', step=1, value=1),
        'extra_people': st.number_input('extra_people', step=0.01, value=0.0),
        'minimum_nights': st.number_input('minimum_nights', step=1, value=1),
        'ano': st.number_input('ano', step=1, value=2023),
        'mes': st.number_input('mes', step=1, value=1),
        'numero_amenities': st.number_input('numero_amenities', step=1, value=5),
        'host_listings_count': st.number_input('host_listings_count', step=1, value=1)
    }

    # Entradas booleanas
    x_tf = {
        'host_is_superhost': 1 if st.selectbox('host_is_superhost', ['Sim', 'Não']) == 'Sim' else 0,
        'instant_bookable': 1 if st.selectbox('instant_bookable', ['Sim', 'Não']) == 'Sim' else 0
    }

    # Entradas categóricas (one-hot)
    x_listas = {
        'property_type': ['Apartment', 'Bed and breakfast', 'Condominium', 'Guest suite', 'Guesthouse', 'Hostel', 'House', 'Loft', 'Outros', 'Serviced apartment'],
        'room_type': ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room'],
        'cancellation_policy': ['flexible', 'moderate', 'strict', 'strict_14_with_grace_period']
    }

    dicionario = {}
    for item in x_listas:
        for valor in x_listas[item]:
            dicionario[f'{item}_{valor}'] = 0
        valor_escolhido = st.selectbox(f'{item}', x_listas[item])
        dicionario[f'{item}_{valor_escolhido}'] = 1

    return x_numericos, x_tf, dicionario

def montar_dataframe(x_numericos, x_tf, dicionario, colunas):
    dicionario.update(x_numericos)
    dicionario.update(x_tf)

    df = pd.DataFrame(dicionario, index=[0])

    # Preenchendo colunas ausentes com zero
    for col in colunas:
        if col not in df.columns:
            df[col] = 0

    # Reordenando as colunas
    df = df[colunas]

    return df

# ========= Execução do App =========

x_numericos, x_tf, dicionario = coleta_inputs()

if st.button("🔍 Prever valor do imóvel"):
    # Lendo os dados de referência
    dados = pd.read_csv("dados.csv")
    colunas = list(dados.columns)[1:-1]

    # Criando o DataFrame de entrada
    valores_x = montar_dataframe(x_numericos, x_tf, dicionario, colunas)

    # Carregando o modelo e prevendo
    modelo = joblib.load('modelo.joblib')
    preco = modelo.predict(valores_x)

    # Exibindo o resultado
    st.success(f"💰 Valor previsto do imóvel: R$ {preco[0]:,.2f}")

