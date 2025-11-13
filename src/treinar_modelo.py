import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib  # <-- Importe o joblib
import import_db as imp

print("Iniciando script de treinamento...")

df = imp.import_banco_de_dados()
print(df)

# 

df_processado = pd.get_dummies(df.drop(['id', 'data'], axis=1, errors='ignore'), drop_first=True)

try:
    X = df_processado.drop('quantidade_pessoas', axis=1)
    y = df_processado['quantidade_pessoas']
except KeyError:
    print("Erro: Coluna 'quantidade_pessoas' não encontrada.")
    print("Colunas disponíveis após o processamento:", df_processado.columns)
    exit()

print("Dividindo dados e iniciando o treinamento...")
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.2, random_state=42)

modelo = RandomForestRegressor(n_estimators=100, random_state=42)
modelo.fit(X_treino, y_treino)

previsoes = modelo.predict(X_teste)
mae = mean_absolute_error(y_teste, previsoes)
print(f"\nTreinamento concluído!")
print(f"O Erro Médio Absoluto (MAE) deste modelo é: {mae:.2f} pessoas")

joblib.dump(modelo, 'modelo_ru.joblib')

joblib.dump(X.columns, 'colunas_modelo.joblib')

print("\nModelo e colunas salvos com sucesso!")
print("Arquivos: 'modelo_ru.joblib' e 'colunas_modelo.joblib'")