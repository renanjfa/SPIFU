import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import df_handler as hand

def import_banco_de_dados():
    password = "Rjfa2708@!"
    senha = quote_plus(password)

    string_conexao = f"mysql+pymysql://root:{senha}@localhost:3306/spifu"
    engine = create_engine(string_conexao)
    query = "SELECT * FROM dados_ru"

    try:
        df = pd.read_sql(query, engine)
        print(f"Dados carregados com sucesso. {len(df)} linhas encontradas.")
    except Exception as e:
        print(f"Erro ao conectar ou carregar dados: {e}")
        exit()

    print(df)
    return df

df = import_banco_de_dados()
hand.criar_colunas_auxiliares(df)
print(df)
hand.preenche_df_list(df)
print(df)

df.to_csv('teste_preencher_lista_df', index=False)
