import os

def carregar_cardapio():
    mapa_pratos = {}
    caminho_arquivo = '../data/CodigosCardapioRU.txt'
    
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8', errors='ignore') as f:
            for linha in f:
                if ' - ' in linha:
                    partes = linha.split(' - ')
                    id_prato = partes[0].strip()
                    nome_prato = partes[1].strip().upper()
                    
                    mapa_pratos[nome_prato] = id_prato
        
        return mapa_pratos

    except FileNotFoundError:
        print(f"⚠️  ERRO: Arquivo '{caminho_arquivo}' não encontrado.")
        return {}

def obter_id(nome_busca, cardapio_dict):
    termo = str(nome_busca).upper().strip()
    
    if termo in cardapio_dict:
        return cardapio_dict[termo]
    
    for nome, id_prato in cardapio_dict.items():
        if termo in nome:
            print(f"   ℹ️  (Auto-correção) Usando '{nome}' para '{termo}'")
            return id_prato
            
    print(f"   ❌ Prato '{termo}' não encontrado no cardápio. Usando 0.")
    return "0"