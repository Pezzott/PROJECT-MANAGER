# modules/cronograma.py

import json

# Função para carregar os dados do cronograma a partir de um arquivo JSON
def load_data(filepath):
    """
    Carrega os dados do cronograma a partir do arquivo JSON especificado.

    Args:
        filepath (str): Caminho para o arquivo JSON do cronograma.

    Returns:
        dict: Dicionário contendo os dados do cronograma.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  # Retorna um dicionário vazio se o arquivo não for encontrado
    except json.JSONDecodeError:
        return {}  # Retorna um dicionário vazio se o JSON estiver malformado

# Função para salvar os dados no arquivo JSON especificado
def save_data(filepath, data):
    """
    Salva os dados no arquivo JSON especificado.

    Args:
        filepath (str): Caminho para o arquivo JSON onde os dados serão salvos.
        data (dict): Dicionário contendo os dados do cronograma.

    Returns:
        bool: Retorna True se o salvamento foi bem-sucedido, False caso contrário.
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return True
    except IOError:
        return False
