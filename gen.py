# -*- coding: utf-8 -*-
"""
gera automaticamente um xlsx com dados de clientes e datas de pagamento
"""
import os
import pandas as pd
import numpy as np


# ------------------------------------------------------------- #
# Diretório de destino
diretorio = r'---' # ADC SEU CAMINHO AQUI
arquivo = 'historico_pagamentos.xlsx'
caminho_completo = os.path.join(diretorio, arquivo)
# ------------------------------------------------------------- #

# ------------------------------------------------------------- #
# Verifica se o diretório existe ou cria ou
os.makedirs(diretorio, exist_ok=True)

# Gera dados fictícios
dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="7D")
data = {
    "Data": dates,
    "Valor": np.random.uniform(50, 500, len(dates)),
    "Status": np.random.choice(["Completo", "Atrasado", "Pendente"], len(dates)),
    "Categoria": np.random.choice(["Alimentação", "Transporte", "Lazer", "Moradia"], len(dates)),
    "Método Pagamento": np.random.choice(["Cartão Crédito", "Boleto", "PIX"], len(dates))
}
# ------------------------------------------------------------- #

# ------------------------------------------------------------- #
# Criar DataFrame e salva
df = pd.DataFrame(data)
df.to_excel(caminho_completo, index=False)
# ------------------------------------------------------------- #

# ------------------------------------------------------------- #
# Print da conclusão
print(f"Arquivo gerado com sucesso em: {caminho_completo}")
# ------------------------------------------------------------- #
