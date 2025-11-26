import pandas as pd
import joblib
import df_handler as hand
import cardapio as menu
from datetime import datetime
import os

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_busca_interativa(dicionario_pratos):
    print("\n🔍 --- CONSULTA DE CARDÁPIO ---")
    print("Dica: Digite uma palavra (ex: 'Batata') para ver as opções.")
    print("      Ou aperte ENTER direto para pular.")
    
    while True:
        termo = input("\n🔎 Pesquisar por (Enter para pular): ").strip().upper()
        if not termo: break 
            
        encontrados = [nome for nome in dicionario_pratos.keys() if termo in nome]
        encontrados.sort()
        
        if encontrados:
            print(f"✅ Encontrei {len(encontrados)} pratos:")
            for item in encontrados[:10]:
                print(f"   • {item}")
            if len(encontrados) > 10:
                print(f"   ... e mais {len(encontrados)-10} opções.")
        else:
            print(f"❌ Nada encontrado com '{termo}'.")

def pedir_input(mensagem, padrao=None):
    texto_padrao = f" [Padrão: {padrao}]" if padrao else ""
    valor = input(f"{mensagem}{texto_padrao}: ").strip()
    if not valor and padrao: return padrao
    return valor

limpar_tela()
print("--- INICIANDO SISTEMA SPIFU ---")

try:
    print("⏳ Carregando modelos de IA...")
    modelo_almoco = joblib.load('../models/modelo_almoco.joblib')
    colunas_almoco = joblib.load('../models/colunas_modelo_almoco.joblib')
    
    modelo_jantar = joblib.load('../models/modelo_jantar.joblib')
    colunas_jantar = joblib.load('../models/colunas_modelo_jantar.joblib')
    
    print("⏳ Carregando cardápio...")
    dicionario = menu.carregar_cardapio()
    print("✅ Sistema pronto!")
    
except FileNotFoundError:
    print("❌ Erro: Arquivos não encontrados. Rode o 'treinar_modelo.py' primeiro.")
    exit()

while True:
    print("\n" + "="*50)
    print("             NOVA PREVISÃO")
    print("     (Digite '0' ou 'SAIR' a qualquer momento)")
    print("="*50)

    hoje = datetime.now().strftime('%Y-%m-%d')
    data_input = input(f"📅 Data (AAAA-MM-DD) [Enter para {hoje}]: ").strip()
    
    if data_input.upper() in ['SAIR', '0', 'EXIT']:
        print("\n👋 Encerrando sistema. Até mais!")
        break
        
    if not data_input:
        data_digitada = hoje
    else:
        data_digitada = data_input

    mostrar_busca_interativa(dicionario)
    
    print("-" * 40)
    prato_input = input("🥘 Nome do Prato Principal: ").strip()
    
    if prato_input.upper() in ['SAIR', '0', 'EXIT']:
        print("\n👋 Encerrando sistema.")
        break

    id_prato = menu.obter_id(prato_input, dicionario)
    
    dados_entrada = {
        'data': [data_digitada],
        'prato_principal': [id_prato],
        'acompanhamento': ['0'], 'guarnicao': ['0'], 
        'sobremesa': ['0'], 'sem_atendimento': [0]
    }

    df_novo = pd.DataFrame(dados_entrada)
    
    try:
        hand.criar_colunas_auxiliares(df_novo)
        hand.preenche_df_list(df_novo)
        
        df_novo['data'] = pd.to_datetime(df_novo['data'])
        df_novo['dia_da_semana'] = df_novo['data'].dt.day_name()
        
        df_processado = pd.get_dummies(df_novo.drop(['data'], axis=1, errors='ignore'))
        
        df_almoco_final = df_processado.reindex(columns=colunas_almoco, fill_value=0)
        prev_almoco = modelo_almoco.predict(df_almoco_final)[0]
        
        df_jantar_final = df_processado.reindex(columns=colunas_jantar, fill_value=0)
        prev_jantar = modelo_jantar.predict(df_jantar_final)[0]

        print("\n" + "="*35)
        print(f"📊  RELATÓRIO: {data_digitada} ({df_novo['dia_da_semana'][0]})")
        print(f"🥘  Prato: {prato_input.upper()} (ID: {id_prato})")
        print("-" * 35)
        print(f"☀️  ALMOÇO: {int(prev_almoco)} pessoas")
        print(f"🌙  JANTAR: {int(prev_jantar)} pessoas")
        print(f"∑   TOTAL:  {int(prev_almoco + prev_jantar)} pessoas")
        print("="*35)
        
    except Exception as e:
        print(f"\n❌ Erro ao processar: {e}")
        print("Verifique se a data está no formato correto.")

    input("\nPRESSIONE ENTER PARA FAZER OUTRA PREVISÃO...")
    limpar_tela() 