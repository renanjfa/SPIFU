import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib
import import_db as imp # Importa o script que acabamos de editar

print("Iniciando script de treinamento...")

# 1. Carrega os dados usando a função do import_db
df = imp.get_data()

print("Colunas disponíveis:", df.columns)

# 2. Pré-processamento
# O Pandas get_dummies vai transformar texto restante em números
df_processado = pd.get_dummies(df.drop(['data'], axis=1, errors='ignore'), drop_first=True)

# 3. Definir o Alvo (CORREÇÃO IMPORTANTE AQUI)
# Você tem 'quantidade_almoco' e 'quantidade_jantar'. 
# Vamos tentar prever o ALMOÇO primeiro.
ALVO = 'quantidade_almoco' 

# Se quiser prever o total, descomente a linha abaixo:
# df_processado['total_pessoas'] = df['quantidade_almoco'] + df['quantidade_jantar']
# ALVO = 'total_pessoas'

try:
    # Removemos o alvo e a outra contagem (jantar) para não "dar a resposta" pro modelo
    X = df_processado.drop(['quantidade_almoco', 'quantidade_jantar'], axis=1, errors='ignore')
    y = df_processado[ALVO]
except KeyError as e:
    print(f"Erro: Coluna {e} não encontrada.")
    exit()

# Remover linhas com valores vazios (NaN) que podem ter sido gerados
X = X.fillna(0)

print("Dividindo dados e iniciando o treinamento...")
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.2, random_state=42)

modelo = RandomForestRegressor(n_estimators=100, random_state=42)
modelo.fit(X_treino, y_treino)

previsoes = modelo.predict(X_teste)
mae = mean_absolute_error(y_teste, previsoes)

print(f"\nTreinamento concluído!")
print(f"O Erro Médio Absoluto (MAE) é: {mae:.2f}")

# Salvar
joblib.dump(modelo, 'modelo_ru.joblib')
joblib.dump(X.columns, 'colunas_modelo.joblib')
print("Modelo salvo com sucesso!")