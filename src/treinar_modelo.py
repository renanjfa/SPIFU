import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib
import import_db as imp

MODEL_PATH = "C:/COMP_UEL/Projetos/SPIFU-main/models/"

print("--- TREINAMENTO SIMPLIFICADO (PRATO + DIA) ---")

df = imp.get_data()

df['data'] = pd.to_datetime(df['data'])
df['dia_da_semana'] = df['data'].dt.day_name() 

print(f"Base carregada: {len(df)} registros.")

def treinar_especifico(df_completo, nome_alvo, nome_arquivo):
    print(f"\n>>> TREINANDO: {nome_alvo.upper()} <<<")

    cols_features = ['dia_da_semana'] + [c for c in df_completo.columns if 'prato_principal' in c]
    
    print(f"Usando apenas as colunas: {cols_features}")
    
    df_focado = df_completo[cols_features].copy()
    
    df_processado = pd.get_dummies(df_focado, drop_first=True)
    
    X = df_processado
    y = df_completo[nome_alvo].fillna(0) 
    
    X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.2, random_state=42)
    
    modelo = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo.fit(X_treino, y_treino)
    
    mae = mean_absolute_error(y_teste, modelo.predict(X_teste))
    print(f"Erro Médio (MAE): {mae:.2f}")
    
    joblib.dump(modelo, MODEL_PATH + f'{nome_arquivo}.joblib')
    joblib.dump(X.columns, MODEL_PATH + f'colunas_{nome_arquivo}.joblib')

treinar_especifico(df, 'quantidade_almoco', 'modelo_almoco')
treinar_especifico(df, 'quantidade_jantar', 'modelo_jantar')