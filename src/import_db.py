import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import df_handler as hand

# def import_banco_de_dados():
#     password = "Rjfa2708@!"
#     senha = quote_plus(password)

#     string_conexao = f"mysql+pymysql://root:{senha}@localhost:3306/spifu"
#     engine = create_engine(string_conexao)
#     query = "SELECT * FROM dados_ru"

#     try:
#         df = pd.read_sql(query, engine)
#         print(f"Dados carregados com sucesso. {len(df)} linhas encontradas.")
#     except Exception as e:
#         print(f"Erro ao conectar ou carregar dados: {e}")
#         exit()

#     print(df)
#     return df

def get_data():
    # Lê o CSV que você enviou
    try:
        df = pd.read_csv('../data/ru_final_limpo.csv')
        print(f"CSV carregado com sucesso. {len(df)} linhas.")
    except FileNotFoundError:
        print("Erro: Arquivo 'ru_final_limpo.csv' não encontrado.")
        exit()
        
    # Aplica o tratamento de colunas (sua lógica do df_handler)
    print("Processando colunas complexas (listas)...")
    hand.criar_colunas_auxiliares(df)
    hand.preenche_df_list(df)


    return df

df = get_data()
print(df)
