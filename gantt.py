import pandas as pd # type: ignore
import plotly.express as px # type: ignore

# Função para criar o gráfico de Gantt a partir dos dados fornecidos
def create_gantt_chart(df):
    df.rename(columns={'name': 'Task', 'start_dev': 'Start', 'end_dev': 'Finish'}, inplace=True)
    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="system", title="Gantt Chart")
    fig.update_yaxes(categoryorder="total ascending")
    return fig.to_html(full_html=False)
