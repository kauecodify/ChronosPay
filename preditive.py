# -*- coding: utf-8 -*-
"""
Faz a previsão com modelos de regressão linear,
cria pipelines e faz o treinamento do modelo com datas futuras
"""
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from datetime import datetime, timedelta
from openpyxl import Workbook
from openpyxl.styles import GradientFill
import os

# ------------------------------------------------------ #
# Configuração dos caminhos 
INPUT_FILE_PATH = r'---' # adc caminhos
OUTPUT_FILE_PATH = r'---' # adc caminhos
# ------------------------------------------------------ #

# ------------------------------------------------------ #
# Lê os dados
print(f"Lendo arquivo: {INPUT_FILE_PATH}")
df = pd.read_excel(INPUT_FILE_PATH)
# ------------------------------------------------------ #

# ------------------------------------------------------ #
# Pré-processamento dos dados
le = LabelEncoder()
for col in ["Status", "Categoria", "Método Pagamento"]:
    if col in df.columns:
        df[col+'_index'] = le.fit_transform(df[col])
# ------------------------------------------------------ #

# ------------------------------------------------------ #
# Treina o modelo
X = df[["Valor", "Status_index", "Categoria_index", "Método Pagamento_index"]]
y = df["Valor"]
model = RandomForestRegressor().fit(X, y)
# ------------------------------------------------------ #

# ------------------------------------------------------ #
# Cria datas futuras
future_dates = [(datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(1, 31)]
future_df = pd.DataFrame(future_dates, columns=["Data"])
# ------------------------------------------------------ #

# ------------------------------------------------------ #
# Faz as previsões
future_df["Valor Previsto"] = model.predict(X[:len(future_dates)])
# ------------------------------------------------------ #

# ------------------------------------------------------ #
# Exporta para Excel
wb = Workbook()
ws = wb.active
ws.append(["Data", "Valor Previsto"])
for row in future_df.itertuples(index=False):
    ws.append(row)
wb.save(OUTPUT_FILE_PATH)
print(f"Arquivo salvo em: {OUTPUT_FILE_PATH}")
# ------------------------------------------------------ #
