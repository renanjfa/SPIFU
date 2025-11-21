import pandas as pd
import numpy as np

def stringToList(valor):
    # 1. Proteção contra NaNs (floats) e valores não-texto
    if not isinstance(valor, str):
        return []
    
    # 2. Limpeza extra: Remove aspas que podem vir do CSV
    valor_limpo = valor.replace('"', '').replace("'", "")
    
    # 3. Divide pela vírgula
    aux = valor_limpo.split(",")
    
    l = []
    for i in aux:
        try:
            # Remove espaços em branco ao redor (ex: " 45 ")
            item_limpo = i.strip()
            
            # Se sobrou algo depois de limpar...
            if item_limpo:
                # TENTA converter. Se falhar (ex: for uma vírgula solta), vai pro except
                item = int(item_limpo)
                l.append(item)
        except ValueError:
            # Se der erro na conversão, apenas ignora e continua o loop
            continue
            
    return l

def criar_colunas_auxiliares(df):
   df.insert(2, 'acompanhamento2', 0)
   df.insert(3, 'acompanhamento3', 0)
   df.insert(5, 'prato_principal2', 0)
   df.insert(6, 'prato_principal3', 0)
   df.insert(8, 'guarnicao2', 0)
   df.insert(9, 'guarnicao3', 0)
   df.insert(11, 'sobremesa2', 0)
   df.insert(12, 'sobremesa3', 0)


def preenche_df_list(df):
    for idx, row in df.iterrows():
        # ----------- acompanhamento ------------- #
        acomp_aux = stringToList(row['acompanhamento'])
        acomp_aux.append(0)

        while len(acomp_aux) < 3:
            acomp_aux.append(0)

        df.loc[idx, 'acompanhamento'] = acomp_aux[0]
        df.loc[idx, 'acompanhamento2'] = acomp_aux[1]
        df.loc[idx, 'acompanhamento3'] = acomp_aux[2]

        # ------------ prato_principal ----------- #
        prato_aux = stringToList(row['prato_principal'])
        prato_aux.append(0)

        while len(prato_aux) < 3:
            prato_aux.append(0)

        df.loc[idx, 'prato_principal'] = prato_aux[0]
        df.loc[idx, 'prato_principal2'] = prato_aux[1]
        df.loc[idx, 'prato_principal3'] = prato_aux[2]

        # ------------ guarnicao --------------- #
        guarnicao_aux = stringToList(row['guarnicao'])
        guarnicao_aux.append(0)

        while len(guarnicao_aux) < 3:
            guarnicao_aux.append(0)

        df.loc[idx, 'guarnicao'] = guarnicao_aux[0]
        df.loc[idx, 'guarnicao2'] = guarnicao_aux[1]
        df.loc[idx, 'guarnicao3'] = guarnicao_aux[2]

        # ------------- sobremesa ------------- #
        sobremesa_aux = stringToList(row['sobremesa'])
        sobremesa_aux.append(0)

        while len(sobremesa_aux) < 3:
            sobremesa_aux.append(0)

        df.loc[idx, 'sobremesa'] = sobremesa_aux[0]
        df.loc[idx, 'sobremesa2'] = sobremesa_aux[1]
        df.loc[idx, 'sobremesa3'] = sobremesa_aux[2]