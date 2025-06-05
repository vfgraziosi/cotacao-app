# 3. ExchangeRate.host
try:
    r = requests.get("https://api.exchangerate.host/latest", params={"base": "USD", "symbols": "BRL"})
    data = r.json()
    if "rates" in data and "BRL" in data["rates"]:
        valor = float(data["rates"]["BRL"])
        resultados.append({
            "Fonte": "ExchangeRate.host",
            "Compra": valor,
            "Venda": valor
        })
    else:
        raise ValueError("Campo 'rates.BRL' não encontrado na resposta.")
except Exception as e:
    resultados.append({
        "Fonte": "ExchangeRate.host",
        "Compra": "Erro",
        "Venda": str(e)
    })
