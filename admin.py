from flask import Flask, render_template, request, jsonify  # type: ignore
import json
from datetime import datetime
import os

# Instância do Flask
admin_app = Flask(__name__, template_folder='templates')

# Caminhos para os arquivos JSON de dados
JSON_FILE_PATH = os.path.join('data', 'cronograma.json')
NOTES_FILE_PATH = os.path.join('data', 'anotacoes.json')

# Função para carregar os dados do cronograma
def load_data():
    try:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "transferencia_veiculos_novos": [],
            "remessa_veiculos_demonstracao": [],
            "outras_tarefas": []
        }

# Função para carregar os dados das anotações
def load_notes():
    try:
        with open(NOTES_FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"anotacoes": []}

# Função para salvar os dados no arquivo JSON de cronograma
def save_data(data):
    with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Função para salvar os dados no arquivo JSON de anotações
def save_notes(notes):
    with open(NOTES_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(notes, f, indent=4, ensure_ascii=False)

# Função para converter data de YYYY-MM-DD para DD/MM/YYYY
def convert_date_format(date_str):
    try:
        if date_str and date_str.upper() != 'N/A':
            return datetime.strptime(date_str, '%Y-%m-%d').strftime('%d/%m/%Y')
        return date_str
    except ValueError:
        return date_str

# Função para converter data de DD/MM/YYYY para YYYY-MM-DD
def convert_date_for_input(date_str):
    try:
        if date_str and date_str.upper() != 'N/A':
            return datetime.strptime(date_str, '%d/%m/%Y').strftime('%Y-%m-%d')
        return date_str
    except ValueError:
        return date_str

# Função para normalizar texto removendo espaços extras e garantindo insensibilidade a maiúsculas/minúsculas
def normalize_text(text):
    return " ".join(text.split()).lower()  # Remove espaços duplicados e converte para minúsculas

# Rota para interface administrativa
@admin_app.route('/admin')
def admin():
    cronograma = load_data()
    return render_template('add_activity.html', cronograma=cronograma)

# Rota para adicionar nova tarefa
@admin_app.route('/add-task', methods=['POST'])
def add_task():
    data = {
        "name": request.form.get("name"),
        "system": request.form.get("system"),
        "start_dev": convert_date_format(request.form.get("start_dev")),
        "end_dev": convert_date_format(request.form.get("end_dev")),
        "progress_dev": request.form.get("progress_dev"),
        "start_test": convert_date_format(request.form.get("start_test")),
        "end_test": convert_date_format(request.form.get("end_test")),
        "progress_test": request.form.get("progress_test"),
        "deployment": convert_date_format(request.form.get("deployment")),
        "responsible": request.form.get("responsible"),
    }

    section = request.form.get('section')
    cronograma_data = load_data()

    if section in cronograma_data:
        cronograma_data[section].append(data)
    else:
        return jsonify({"error": "Seção inválida"}), 400

    save_data(cronograma_data)
    return jsonify({"message": "Tarefa adicionada com sucesso!"}), 200

# Rota para buscar todas as tarefas de uma seção específica
@admin_app.route('/get-tasks', methods=['GET'])
def get_tasks():
    section = request.args.get('section')
    cronograma_data = load_data()

    # Normaliza a seção antes de buscar
    if normalize_text(section) in [normalize_text(sec) for sec in cronograma_data.keys()]:
        return jsonify({"tasks": cronograma_data[section]}), 200
    return jsonify({"error": "Seção não encontrada!"}), 404

# Rota para buscar os detalhes de uma tarefa específica para edição
@admin_app.route('/get-task', methods=['POST'])
def get_task():
    section = request.form.get('section')
    task_name = request.form.get('task_name')
    
    # Verifique se a seção e o nome da tarefa estão sendo recebidos
    print("Recebendo dados: ", section, task_name)

    cronograma_data = load_data()
    if section in cronograma_data:
        for task in cronograma_data[section]:
            if normalize_text(task['name']) == normalize_text(task_name):
                print("Tarefa encontrada:", task)
                task['start_dev'] = convert_date_for_input(task.get('start_dev'))
                task['end_dev'] = convert_date_for_input(task.get('end_dev'))
                task['start_test'] = convert_date_for_input(task.get('start_test'))
                task['end_test'] = convert_date_for_input(task.get('end_test'))
                task['deployment'] = convert_date_for_input(task.get('deployment'))
                return jsonify({"task": task}), 200
    return jsonify({"error": "Tarefa não encontrada!"}), 404

# Rota para editar uma tarefa existente
@admin_app.route('/edit-task', methods=['POST'])
def edit_task():
    section = request.form.get('section')
    task_name = request.form.get('task_name')

    updated_data = {
        "name": request.form.get("name"),
        "system": request.form.get("system"),
        "start_dev": convert_date_format(request.form.get("start_dev")),
        "end_dev": convert_date_format(request.form.get("end_dev")),
        "progress_dev": request.form.get("progress_dev"),
        "start_test": convert_date_format(request.form.get("start_test")),
        "end_test": convert_date_format(request.form.get("end_test")),
        "progress_test": request.form.get("progress_test"),
        "deployment": convert_date_format(request.form.get("deployment")),
        "responsible": request.form.get("responsible"),
    }

    cronograma_data = load_data()
    if section in cronograma_data:
        for task in cronograma_data[section]:
            if normalize_text(task['name']) == normalize_text(task_name):
                task.update(updated_data)
                save_data(cronograma_data)
                return jsonify({"message": "Tarefa atualizada com sucesso!"}), 200

    return jsonify({"error": "Falha ao atualizar a tarefa!"}), 400

# Rota para buscar uma anotação específica
@admin_app.route('/get-note', methods=['POST'])
def get_note():
    category = request.form.get('category')
    activity = request.form.get('activity')
    print(f"Categoria recebida: {category}, Atividade recebida: {activity}")  # Adicionar log para verificar os dados recebidos

    notes_data = load_notes()
    for note in notes_data['anotacoes']:
        print(f"Verificando anotação: {note['categoria']} - {note['atividade']}")  # Log adicional
        if normalize_text(note['categoria']) == normalize_text(category) and normalize_text(note['atividade']) == normalize_text(activity):
            print(f"Anotação encontrada: {note['anotacoes']}")  # Verificar qual anotação foi encontrada
            return jsonify({"note": note['anotacoes']}), 200

    print("Anotação não encontrada!")  # Log para saber se não encontrou a anotação
    return jsonify({"note": []}), 200

# Rota para salvar uma nova anotação ou atualizar uma existente
@admin_app.route('/save-note', methods=['POST'])
def save_note():
    category = request.form.get('category')
    activity = request.form.get('activity')
    new_note = request.form.get('note')

    print(f"Recebendo nova anotação para salvar: Categoria - {category}, Atividade - {activity}, Nota - {new_note}")  # Log inicial

    notes_data = load_notes()
    found = False

    for note in notes_data['anotacoes']:
        if normalize_text(note['categoria']) == normalize_text(category) and normalize_text(note['atividade']) == normalize_text(activity):
            note['anotacoes'] = [new_note]  # Substituir anotação
            found = True
            print(f"Anotação atualizada: {note}")  # Verificar se a anotação foi atualizada corretamente
            break

    if not found:
        new_entry = {
            "atividade": normalize_text(activity),
            "categoria": normalize_text(category),
            "anotacoes": [new_note]
        }
        notes_data['anotacoes'].append(new_entry)
        print(f"Nova anotação adicionada: {new_entry}")  # Log para nova anotação

    save_notes(notes_data)
    print("Notas após salvar:", notes_data)  # Verificar como está o JSON após salvar
    return jsonify({"message": "Anotação salva com sucesso!"}), 200

# Função para rodar a instância do admin
if __name__ == '__main__':
    admin_app.run(port=5001)
