import pandas as pd
import plotly.express as px
import plotly.offline as plt

# idk man maybe add arguments to each generator? like,, generate_bar_graph(arg1, arg2)? this is for the flexibility and customization of the data vis

data = pd.read_csv('test_data/dummy_data.csv')

def generate_bar_graph():
    average_scores = data.groupby("Religion")["Mental Health Score"].mean().reset_index()

    fig = px.bar (
        average_scores, x="Religion", y="Mental Health Score", height=600, width=1200, 
        title='Data Test',
        color="Religion", color_discrete_sequence=['#DB9050', '#095371', '#6092C0', 'teal'])
    
    fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
        
    result = fig.to_html(include_plotlyjs=False)

    return result

def generate_pie_graph():
    fig = px.pie(data, names='Gender', 
            height=300, width=600, 
            title='IDENTITY',
            color_discrete_sequence=['#DB9050', '#095371', '#6092C0'])

    fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
        
    result = fig.to_html(include_plotlyjs=False)

    return result

def generate_scatter_plot():
    fig = px.scatter(
        data, 
        x="Mental Health Score", 
        y="GPA",
        color="GPA",
        color_continuous_scale=['#DB9050', '#095371', '#6092C0', 'lime'],
        height=300, width=900, 
    )

    result = fig.to_html(include_plotlyjs=False)

    return result