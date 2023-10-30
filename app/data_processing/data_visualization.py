import os
import pandas as pd
import plotly.express as px

data_directory = os.path.join(os.path.dirname(__file__), 'data')

dummy_data_past = os.path.join(data_directory, 'dummy_data.csv')
dummy_data_new= os.path.join(data_directory, 'new_data.csv')

data_past = pd.read_csv(dummy_data_past)
data_new = pd.read_csv(dummy_data_new)

def process_data_past(first_metric, second_metric):
    data = pd.read_csv(dummy_data_past)

    # calculates the mean
    # TODO: nag eerror sa mga percentage and non-numerical value
    average_scores = data.groupby(first_metric)[second_metric].mean().reset_index()
    data_average = average_scores.to_dict(orient='records')

    return data_average

def process_data_new(first, second):
    data = pd.read_csv(dummy_data_new)

    # calculates the mean
    # TODO: nag eerror sa mga percentage and non-numerical value
    average_scores = data.groupby(first)[second].mean().reset_index()
    data_average = average_scores.to_dict(orient='records')

    return data_average