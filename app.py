import streamlit as st
import requests

st.set_page_config(page_title="Cotação do Dólar", layout="centered")
st.title("💵 Cotação do Dólar – Compra e Venda")

if st.button("🔍 Consultar cotações"):
    resultados = []

    # 1. AwesomeAPI
    try:
        r = requests.get("https://economia.awesomeapi.com.br/json/last/USD-BRL")
        data = r.json()["USDBRL"]
        resultados.append({
            "Fonte": "AwesomeAPI",
            "Compra": float(data["bid"]),
            "Venda": float(data["ask"])
        })
    except Exception as e:
        resultados.append({
            "Fonte": "AwesomeAPI",
            "Compra": "Erro",
            "Venda": str(e)
        })

    # 2. Banco Central (via SGS API)
    try:
        r = requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados/ultimos/1?formato=json")
        data = r.json()[0]
        valor = float(data["valor"])
        resultados.append({
            "Fonte": "Banco Central",
            "Compra": valor,
            "Venda": valor
        })
    except Exception as e:
        resultados.append({
            "Fonte": "Banco Central",
            "Compra": "Erro",
            "Venda": str(e)
        })

    # 3. ExchangeRate.host
    try:
        r = requests.get("https://api.exchangerate.host/latest?base=USD&symbols=BRL")
        data = r.json()
        valor = float(data["rates"]["BRL"])
        resultados.append({
            "Fonte": "ExchangeRate.host",
            "Compra": valor,
            "Venda": valor
        })
    except Exception as e:
        resultados.append({
            "Fonte": "ExchangeRate.host",
            "Compra": "Erro",
            "Venda": str(e)
        })

    st.write("### 💹 Resultado")
    st.table(resultados)
