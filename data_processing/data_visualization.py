
import pandas as pd
import plotly.express as px
import plotly.offline as plt

def generate_bar_graph():
    data_test = pd.read_csv('test_data/dummy_data.csv')

    average_scores = data_test.groupby("Religion")["Mental Health Score"].mean().reset_index()

    fig = px.bar (
        average_scores, x="Religion", y="Mental Health Score", height=600, width=1200, 
        title='Data Test',
        color="Religion", color_discrete_sequence=['#DB9050', '#095371', '#6092C0', 'teal'])
    
    fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
        
    result = fig.to_html(include_plotlyjs=False)

    return result

def generate_pie_graph():
    data = pd.read_csv('test_data/dummy_data.csv')


    fig = px.pie(data, names='Gender', 
            height=300, width=600, 
            title='IDENTITY',
            color_discrete_sequence=['#DB9050', '#095371', '#6092C0'])

    fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
        
    result = fig.to_html(include_plotlyjs=False)

    return result