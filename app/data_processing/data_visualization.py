import os
import pandas as pd
import plotly.express as px

data_directory = os.path.join(os.path.dirname(__file__), 'data')

dummy_data = os.path.join(data_directory, 'dummy_data.csv')

data = pd.read_csv(dummy_data)


def process_data(first_metric, second_metric):
    data = pd.read_csv(dummy_data)

    # calculates the mean
    # TODO: nag eerror sa mga percentage and non-numerical value
    average_scores = data.groupby(first_metric)[second_metric].mean().reset_index()
    data_average = average_scores.to_dict(orient='records')

    return data_average

