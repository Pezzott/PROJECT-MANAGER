import json

# Função para carregar as anotações do arquivo JSON
def load_annotations(filepath):
    """
    Carrega as anotações do arquivo especificado.
    
    Args:
        filepath (str): Caminho para o arquivo JSON das anotações.
    
    Returns:
        dict: Dicionário contendo as anotações.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {'anotacoes': []}  # Retorna um dicionário vazio se o arquivo não for encontrado
    except json.JSONDecodeError:
        return {'anotacoes': []}  # Retorna um dicionário vazio se o JSON estiver malformado

# Função para salvar as anotações no arquivo JSON
def save_annotations(filepath, data):
    """
    Salva as anotações no arquivo especificado.
    
    Args:
        filepath (str): Caminho para o arquivo JSON onde as anotações serão salvas.
        data (dict): Dicionário contendo os dados das anotações.
    
    Returns:
        bool: Retorna True se o salvamento foi bem-sucedido, False caso contrário.
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return True
    except IOError:
        return False
