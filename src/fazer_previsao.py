import pandas as pd
import joblib
import df_handler as hand # Usa suas funções de limpeza
import numpy as np

print("--- Iniciando Previsão do R.U ---")

# 1. CARREGAR O CÉREBRO (O Modelo treinado)
try:
    modelo = joblib.load('modelo_ru.joblib')
    colunas_treino = joblib.load('colunas_modelo.joblib')
    print("✅ Modelo carregado com sucesso.")
except FileNotFoundError:
    print("❌ Erro: Você precisa rodar o 'treinar_modelo.py' antes para gerar o arquivo .joblib")
    exit()

# 2. DEFINIR O CENÁRIO (O "Dia da Lasanha")
# Aqui você coloca os códigos (IDs) dos pratos que quer simular.
# IMPORTANTE: Use o formato de STRING com vírgulas, igual ao CSV original.
dados_entrada = {
    'data': ['2025-11-26'], # A data futura (importante para saber dia da semana)
    
    'prato_principal': ['52'], # <--- COLOQUE O ID DA LASANHA AQUI
    
    'acompanhamento': ['45,46'], # Arroz e Feijão (exemplo)
    'guarnicao': ['54'],         # Ex: Salada
    'sobremesa': ['152'],         # Ex: Gelatina
    'sem_atendimento': [0],
    # A quantidade_almoco/jantar não entra aqui, pois é isso que queremos descobrir!
}

# Transforma o dicionário em DataFrame (Tabela)
df_novo = pd.DataFrame(dados_entrada)

# 3. PROCESSAMENTO (A Mágica do seu df_handler)
# Precisamos aplicar as mesmas transformações que fizemos no treino
print("Processando dados de entrada...")

# A) Cria as colunas vazias (acompanhamento2, 3, etc)
hand.criar_colunas_auxiliares(df_novo)

# B) Separa os IDs (ex: "45,46" vira colunas 45 e 46)
hand.preenche_df_list(df_novo)

# C) Remove colunas de data se o treino removeu
# (O get_dummies do treino removeu 'data' e 'id')
df_processado = pd.get_dummies(df_novo.drop(['data'], axis=1, errors='ignore'))

# 4. ALINHAMENTO FINAL (O Passo de Segurança)
# Garante que a tabela nova tenha EXATAMENTE as mesmas colunas que o modelo conhece.
# Se faltar coluna, ele cria com 0. Se sobrar, ele remove.
df_final = df_processado.reindex(columns=colunas_treino, fill_value=0)

# 5. PREVISÃO
previsao = modelo.predict(df_final)

print("\n" + "="*40)
print(f"🍽️  PREVISÃO PARA O PRATO {dados_entrada['prato_principal'][0]}")
print("="*40)
print(f"👥 Quantidade estimada de pessoas: {int(previsao[0])}")
print("="*40)