# modules/risco.py

import json

def load_risk_data(filepath):
    """
    Carrega os dados de riscos a partir do arquivo JSON especificado.

    Args:
        filepath (str): Caminho para o arquivo JSON dos riscos.

    Returns:
        dict: Dicionário contendo os dados de riscos.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {'riscos': []}  # Retorna um dicionário vazio se o arquivo não for encontrado
    except json.JSONDecodeError:
        return {'riscos': []}  # Retorna um dicionário vazio se o JSON estiver malformado

def save_risk_data(filepath, data):
    """
    Salva os dados de riscos no arquivo JSON especificado.

    Args:
        filepath (str): Caminho para o arquivo JSON onde os riscos serão salvos.
        data (dict): Dicionário contendo os dados dos riscos a serem salvos.

    Returns:
        bool: Retorna True se o salvamento foi bem-sucedido, False caso contrário.
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Erro ao salvar os dados de risco: {e}")
        return False
