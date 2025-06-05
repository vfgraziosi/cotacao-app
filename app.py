
import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Cotação do Dólar", page_icon="💰", layout="centered")

st.title("💸 Cotação do Dólar (Compra e Venda)")
st.markdown("Consulta atualizada de fontes confiáveis: Banco Central, UOL e Google.")

def buscar_bcb():
    try:
        data = datetime.now().strftime('%m-%d-%Y')
        url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/" \
              f"CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='{data}'&$format=json"
        response = requests.get(url)
        response.raise_for_status()
        cotacao = response.json()['value'][0]
        return {
            'Fonte': 'Banco Central do Brasil',
            'Compra (R$)': cotacao['cotacaoCompra'],
            'Venda (R$)': cotacao['cotacaoVenda']
        }
    except Exception as e:
        return {'Fonte': 'Banco Central do Brasil', 'Erro': str(e)}

def buscar_uol():
    try:
        url = "https://economia.uol.com.br/cotacoes/cambio/dolar-estados-unidos/"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        tabela = soup.find('table')
        linhas = tabela.find_all('tr')
        for linha in linhas:
            colunas = linha.find_all('td')
            if colunas and 'Comercial' in colunas[0].text:
                compra = float(colunas[1].text.replace(',', '.'))
                venda = float(colunas[2].text.replace(',', '.'))
                return {
                    'Fonte': 'UOL Economia',
                    'Compra (R$)': compra,
                    'Venda (R$)': venda
                }
        return {'Fonte': 'UOL Economia', 'Erro': 'Dados não encontrados'}
    except Exception as e:
        return {'Fonte': 'UOL Economia', 'Erro': str(e)}

def buscar_google():
    try:
        url = "https://www.google.com/search?q=cotação+dólar"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        span = soup.find("span", {"class": "DFlfde", "data-precision": "2"})
        if span:
            valor = float(span.text.replace(',', '.'))
            return {
                'Fonte': 'Google',
                'Compra (R$)': valor,
                'Venda (R$)': valor
            }
        return {'Fonte': 'Google', 'Erro': 'Valor não encontrado'}
    except Exception as e:
        return {'Fonte': 'Google', 'Erro': str(e)}

if st.button("🔍 Consultar cotações"):
    with st.spinner("Consultando fontes..."):
        dados = [buscar_bcb(), buscar_uol(), buscar_google()]
        df = pd.DataFrame(dados)
        st.success("Consulta finalizada com sucesso!")
        st.table(df)

