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
        compra = f"R$ {float(data['bid']):.4f}"
        venda = f"R$ {float(data['ask']):.4f}"
        resultados.append({
            "Fonte": "AwesomeAPI",
            "Compra": compra,
            "Venda": venda
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
            "Compra": f"R$ {valor:.4f}",
            "Venda": f"R$ {valor:.4f}"
        })
    except Exception as e:
        resultados.append({
            "Fonte": "Banco Central",
            "Compra": "Erro",
            "Venda": str(e)
        })

    # 3. ExchangeRate.host
    try:
        r = requests.get("https://api.exchangerate.host/latest", params={"base": "USD", "symbols": "BRL"})
        data = r.json()
        if "rates" in data and "BRL" in data["rates"]:
            valor = float(data["rates"]["BRL"])
            resultados.append({
                "Fonte": "ExchangeRate.host",
                "Compra": f"R$ {valor:.4f}",
                "Venda": f"R$ {valor:.4f}"
            })
        else:
            raise ValueError("Campo 'rates.BRL' não encontrado na resposta.")
    except Exception as e:
        resultados.append({
            "Fonte": "ExchangeRate.host",
            "Compra": "Erro",
            "Venda": str(e)
        })

    st.write("### 💹 Resultado")
    st.table(resultados)
