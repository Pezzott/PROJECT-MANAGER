import json

def load_pareto_data(filepath):
    """
    Carrega os dados de Pareto a partir de um arquivo JSON.

    Args:
        filepath (str): Caminho para o arquivo JSON.

    Returns:
        dict: Dicionário contendo os dados de Pareto.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}
