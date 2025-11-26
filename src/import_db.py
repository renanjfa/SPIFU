import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import df_handler as hand

def get_data():
    try:
        df = pd.read_csv('../data/ru_final_limpo.csv')
        print(f"CSV carregado com sucesso. {len(df)} linhas.")
    except FileNotFoundError:
        print("Erro: Arquivo 'ru_final_limpo.csv' não encontrado.")
        exit()
        
    print("Processando colunas complexas (listas)...")
    hand.criar_colunas_auxiliares(df)
    hand.preenche_df_list(df)

    return df

df = get_data()
print(df)
