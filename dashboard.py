# -*- coding: utf-8 -*-
"""
Dashboard Completo de Análise de Previsão de Pagamentos
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import FuncFormatter

# ------------------------------------------------------ #
# CONFIGURAÇÕES PRINCIPAIS
# ------------------------------------------------------ #
INPUT_FILE = r'---' # adc caminho output dos dados de previsão
OUTPUT_DASHBOARD = r'---' # adc pasta origem do png com .png
# ------------------------------------------------------ #

# ------------------------------------------------------ #
# FUNÇÕES AUXILIARES
# ------------------------------------------------------ #
def format_currency(x, pos):
    """Formata valores como moeda brasileira"""
    return f'R${x:,.2f}'

def load_and_prepare_data(filepath):
    """Carrega e prepara os dados para análise"""
    df = pd.read_excel(filepath)
    df['Data'] = pd.to_datetime(df['Data'])
    df['Dia da Semana'] = df['Data'].dt.day_name()
    df['Dia do Mês'] = df['Data'].dt.day
    df['Mês'] = df['Data'].dt.month_name()
    return df
# ------------------------------------------------------ #

# ------------------------------------------------------ #
# CONFIGURAÇÃO DO AMBIENTE VISUAL
# ------------------------------------------------------ #
plt.style.use('ggplot')
sns.set_theme(style="whitegrid", palette="husl")
plt.rcParams['figure.figsize'] = [15, 10]
plt.rcParams['font.size'] = 12
# ------------------------------------------------------ #

# ------------------------------------------------------ #
# CARREGAMENTO DOS DADOS
# ------------------------------------------------------ #
try:
    df = load_and_prepare_data(INPUT_FILE)
    print("✅ Dados carregados com sucesso!")
except Exception as e:
    print(f"❌ Erro ao carregar dados: {e}")
    exit()
# ------------------------------------------------------ #

# ------------------------------------------------------ #
# CRIAÇÃO DO DASHBOARD
# ------------------------------------------------------ #
fig = plt.figure(constrained_layout=True, figsize=(18, 12))
gs = GridSpec(3, 3, figure=fig)

# Título principal
fig.suptitle('Dashboard de Previsão de Pagamentos\nAnálise dos Próximos 30 Dias', 
             fontsize=18, fontweight='bold')

# ------------------------------------------------------ #
# GRÁFICO 1: SÉRIE TEMPORAL
# ------------------------------------------------------ #
ax1 = fig.add_subplot(gs[0, :])
sns.lineplot(data=df, x='Data', y='Valor Previsto', marker='o', ax=ax1)
ax1.set_title('Evolução Diária dos Pagamentos Previstos')
ax1.set_xlabel('Data')
ax1.set_ylabel('Valor Previsto')
ax1.yaxis.set_major_formatter(FuncFormatter(format_currency))
ax1.grid(True)

# Destaque para os maiores valores
top_days = df.nlargest(3, 'Valor Previsto')
for _, row in top_days.iterrows():
    ax1.annotate(f'R${row["Valor Previsto"]:,.2f}', 
                xy=(row['Data'], row['Valor Previsto']),
                xytext=(10, 10), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                arrowprops=dict(arrowstyle='->'))

# ------------------------------------------------------ #
# GRÁFICO 2: DISTRIBUIÇÃO SEMANAL
# ------------------------------------------------------ #
ax2 = fig.add_subplot(gs[1, 0])
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
sns.boxplot(data=df, x='Dia da Semana', y='Valor Previsto', order=weekday_order, ax=ax2)
ax2.set_title('Distribuição por Dia da Semana')
ax2.set_xlabel('Dia da Semana')
ax2.set_ylabel('Valor Previsto')
ax2.yaxis.set_major_formatter(FuncFormatter(format_currency))
plt.setp(ax2.get_xticklabels(), rotation=45)

# ------------------------------------------------------ #
# GRÁFICO 3: TOP 5 DIAS
# ------------------------------------------------------ #
ax3 = fig.add_subplot(gs[1, 1])
top_days = df.nlargest(5, 'Valor Previsto')[['Data', 'Valor Previsto']].copy()
top_days['Data'] = top_days['Data'].dt.strftime('%d/%m')
sns.barplot(data=top_days, x='Valor Previsto', y='Data', palette='Blues_d', ax=ax3)
ax3.set_title('Top 5 Dias com Maiores Pagamentos')
ax3.set_xlabel('Valor Previsto')
ax3.set_ylabel('Data')
ax3.xaxis.set_major_formatter(FuncFormatter(format_currency))

# ------------------------------------------------------ #
# GRÁFICO 4: HISTOGRAMA
# ------------------------------------------------------ #
ax4 = fig.add_subplot(gs[1, 2])
sns.histplot(df['Valor Previsto'], kde=True, bins=10, ax=ax4)
ax4.set_title('Distribuição dos Valores Previstos')
ax4.set_xlabel('Valor Previsto')
ax4.set_ylabel('Frequência')
ax4.xaxis.set_major_formatter(FuncFormatter(format_currency))

# ------------------------------------------------------ #
# GRÁFICO 5: AGREGADO SEMANAL
# ------------------------------------------------------ #
ax5 = fig.add_subplot(gs[2, :])
weekly = df.resample('W', on='Data')['Valor Previsto'].sum().reset_index()
sns.barplot(data=weekly, x='Data', y='Valor Previsto', palette='viridis', ax=ax5)
ax5.set_title('Total de Pagamentos Previstos por Semana')
ax5.set_xlabel('Semana')
ax5.set_ylabel('Total Previsto')
ax5.yaxis.set_major_formatter(FuncFormatter(format_currency))
plt.setp(ax5.get_xticklabels(), rotation=45)

# ------------------------------------------------------ #
# MÉTRICAS RESUMO
# ------------------------------------------------------ #
total_previsto = df['Valor Previsto'].sum()
media_diaria = df['Valor Previsto'].mean()
dias_acima_media = (df['Valor Previsto'] > media_diaria).sum()

metrics_text = f"""
Resumo das Previsões:
- Total Previsto (30 dias): R${total_previsto:,.2f}
- Média Diária: R${media_diaria:,.2f}
- Dias Acima da Média: {dias_acima_media}
- Dia com Maior Pagamento: {df.loc[df['Valor Previsto'].idxmax(), 'Data'].strftime('%d/%m')} (R${df['Valor Previsto'].max():,.2f})
"""

fig.text(0.1, 0.05, metrics_text, fontsize=12, bbox=dict(facecolor='lightgray', alpha=0.5))

# ------------------------------------------------------ #
# SALVAMENTO DO DASHBOARD
# ------------------------------------------------------ #
try:
    plt.tight_layout()
    plt.savefig(OUTPUT_DASHBOARD, dpi=300, bbox_inches='tight')
    print(f"✅ Dashboard salvo com sucesso em: {OUTPUT_DASHBOARD}")
except Exception as e:
    print(f"❌ Erro ao salvar dashboard: {e}")

plt.show()
# ------------------------------------------------------ #
# -----------------debbug------------------------------- #
# ------------------------------------------------------ #