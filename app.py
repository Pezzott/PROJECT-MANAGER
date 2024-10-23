# Importações necessárias para a aplicação
from flask import Flask, render_template, request, redirect, jsonify, url_for  # type: ignore
from flask_bootstrap import Bootstrap  # type: ignore
from flask_admin import Admin  # type: ignore
import os
import json

# Importação das funções dos módulos existentes
from modules.cronograma import load_data, save_data
from modules.risco import load_risk_data, save_risk_data
from modules.pareto import load_pareto_data
from modules.gantt import create_gantt_chart
# Novo módulo para carregar e salvar anotações
from modules.annotations import load_annotations, save_annotations

# Configuração e inicialização da aplicação Flask
app = Flask(__name__)
Bootstrap(app)
admin = Admin(app, name='Project Admin', template_mode='bootstrap4')

# Diretórios e arquivos utilizados no projeto
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CRONOGRAMA_FILE = os.path.join(BASE_DIR, 'data', 'cronograma.json')
ANOTACOES_FILE = os.path.join(BASE_DIR, 'data', 'anotacoes.json')
RISCOS_FILE = os.path.join(BASE_DIR, 'data', 'analise_riscos.json')
PARETO_FILE = os.path.join(BASE_DIR, 'data', 'pareto_priorities.json')

# Rota principal para exibir o cronograma
@app.route('/')
def index():
    cronograma_data = load_data(CRONOGRAMA_FILE)
    return render_template('index.html', cronograma=cronograma_data)

# API para carregar as atividades dinamicamente
@app.route('/activities')
def get_activities():
    cronograma_data = load_data(CRONOGRAMA_FILE)
    return jsonify(cronograma_data)

# Rota para editar uma atividade existente
@app.route('/edit/<string:category>/<int:activity_id>', methods=['GET', 'POST'])
def edit_activity(category, activity_id):
    cronograma_data = load_data(CRONOGRAMA_FILE)
    if category == "transferencia_veiculos_novos":
        activity = cronograma_data['transferencia_veiculos_novos'][activity_id]
    elif category == "remessa_veiculos_demonstracao":
        activity = cronograma_data['remessa_veiculos_demonstracao'][activity_id]
    else:
        activity = cronograma_data['outras_tarefas'][activity_id]

    if request.method == 'POST':
        # Atualizar os dados conforme o formulário
        activity['name'] = request.form['name']
        activity['system'] = request.form['system']
        activity['start_dev'] = request.form['start_dev']
        activity['end_dev'] = request.form['end_dev']
        activity['progress_dev'] = request.form['progress_dev']
        activity['start_test'] = request.form['start_test']
        activity['end_test'] = request.form['end_test']
        activity['progress_test'] = request.form['progress_test']
        activity['deployment'] = request.form['deployment']
        activity['progress_deployment'] = request.form['progress_deployment']
        activity['responsible'] = request.form['responsible']

        save_data(CRONOGRAMA_FILE, cronograma_data)
        return redirect(url_for('index'))

    return render_template('edit_activity.html', activity=activity, category=category, activity_id=activity_id)

# Rota para exibir o gráfico de Gantt
@app.route('/gantt')
def gantt_chart():
    cronograma_data = load_data(CRONOGRAMA_FILE)
    return render_template('gantt.html', gantt_html=create_gantt_chart(cronograma_data['transferencia_veiculos_novos']))

# Rota para fornecer os dados das tarefas filtradas para o Gantt Chart
@app.route('/tasks')
def get_tasks():
    category = request.args.get('category')
    pareto_data = load_pareto_data(PARETO_FILE)

    if category in pareto_data:
        prioridades = pareto_data[category]["prioridades"]
        total_impacto = sum([p["impacto"] for p in prioridades])
        cumulative_percentage = 0
        for item in prioridades:
            cumulative_percentage += (item["impacto"] / total_impacto) * 100
            item["cumulative_percentage"] = cumulative_percentage

        return jsonify(prioridades)
    else:
        return jsonify([]), 404

# Nova rota para exibir a análise de Pareto
@app.route('/pareto')
def pareto_chart():
    pareto_data = load_pareto_data(PARETO_FILE)
    category = request.args.get('category', 'transferencia_veiculos_novos')

    if category in pareto_data:
        prioridades = pareto_data[category]["prioridades"]
        return render_template('pareto.html', pareto_data=prioridades)
    else:
        return render_template('pareto.html', message="Categoria inválida.")

# Rota para carregar os riscos da análise de risco
@app.route('/riscos')
def get_riscos():
    riscos_data = load_risk_data(RISCOS_FILE)
    return jsonify(riscos_data)

# Rota para adicionar ou editar um risco
@app.route('/riscos', methods=['POST'])
def update_risco():
    riscos_data = load_risk_data(RISCOS_FILE)
    novo_risco = request.json
    riscos_data['riscos'].append(novo_risco)
    save_risk_data(RISCOS_FILE, riscos_data)
    return jsonify({"status": "success"}), 201

# Rota para buscar anotações por atividade
@app.route('/get_annotations', methods=['GET'])
def get_annotations():
    # Recebe o nome da atividade e a categoria como parâmetros
    activity_name = request.args.get('activity')
    category = request.args.get('category')

    # Ajuste para usar o nome correto das categorias
    category_mapping = {
        'transferencia': 'transferencia_veiculos_novos',
        'remessa': 'remessa_veiculos_demonstração',
        'outras-tarefas': 'outras_tarefas'
    }
    
    # Verifica se a categoria simplificada corresponde a uma categoria no JSON
    category_full_name = category_mapping.get(category, category)

    # Verifica se os parâmetros foram recebidos corretamente
    print(f"Nome da Atividade: {activity_name}, Categoria: {category_full_name}")

    # Carregar anotações do arquivo JSON
    anotacoes_data = load_annotations(ANOTACOES_FILE)

    # Procurar as anotações correspondentes à atividade e categoria
    anotacoes = [
        item['anotacoes'] for item in anotacoes_data['anotacoes']
        if item['atividade'].strip().lower() == activity_name.strip().lower() and
        item['categoria'].strip().lower() == category_full_name.strip().lower()
    ]

    # Se encontrar as anotações, retorna-as, caso contrário, retorna uma lista vazia
    if anotacoes:
        return jsonify({'anotacoes': anotacoes[0]})
    else:
        return jsonify({'anotacoes': []})

# Função para verificar se a aplicação está no ambiente principal
if __name__ == '__main__':
    app.run(port=5000, debug=True)
