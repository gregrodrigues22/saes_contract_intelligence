import pandas as pd

def validar_campos_obrigatorios(caminho_arquivo, campos_esperados):
    try:
        df = pd.read_excel(caminho_arquivo)
        colunas = df.columns.tolist()
        return all(campo in colunas for campo in campos_esperados)
    except Exception as e:
        print(f"Erro ao validar a planilha: {e}")
        return False