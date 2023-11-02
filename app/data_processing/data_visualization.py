import os
import pandas as pd
import plotly.express as px

data_directory = os.path.join(os.path.dirname(__file__), 'data')

# Analytics
dummy_data_past = os.path.join(data_directory, 'dummy_data.csv')
dummy_data_new= os.path.join(data_directory, 'new_data.csv')

# Dashboard
dummy_data_college_sum= os.path.join(data_directory, 'college_count.csv')

data_past = pd.read_csv(dummy_data_past)
data_new = pd.read_csv(dummy_data_new)
data_college_sum = pd.read_csv(dummy_data_college_sum)

# For Past Data
def process_data_past(first_metric, second_metric):
    data = pd.read_csv(dummy_data_past)

    # calculates the mean
    # TODO: nag eerror sa mga percentage and non-numerical value
    average_scores = data.groupby(first_metric)[second_metric].mean().reset_index()
    data_average = average_scores.to_dict(orient='records')

    return data_average

# For New Data
def process_data_new(first, second):
    data = pd.read_csv(dummy_data_new)

    # calculates the mean
    # TODO: nag eerror sa mga percentage and non-numerical value
    average_scores = data.groupby(first)[second].mean().reset_index()
    data_average = average_scores.to_dict(orient='records')

    return data_average

# For College Summaries
def process_data_college_sum():
    data = pd.read_csv(dummy_data_college_sum)

    average_scores = data.groupby('Colleges')['Students'].mean().reset_index()
    data_average = average_scores.to_dict(orient='records')

    return data_average

# For Nature of Concern
def process_data_concern():
    data = pd.read_csv(dummy_data_college_sum)

    average_scores = data.groupby('Concern')['Students'].mean().reset_index()
    data_average = average_scores.to_dict(orient='records')

    return data_average

# For Campus
def process_data_campus():
    data = pd.read_csv(dummy_data_college_sum)

    average_scores = data.groupby('Campus')['Students'].mean().reset_index()
    data_average = average_scores.to_dict(orient='records')

    return data_average

# For Identity 
def process_data_identity():
    data = pd.read_csv(dummy_data_college_sum)

    average_scores = data.groupby('Identity')['Students'].mean().reset_index()
    data_average = average_scores.to_dict(orient='records')

    return data_average

# For Religion
def process_data_religion():
    data = pd.read_csv(dummy_data_college_sum)

    average_scores = data.groupby('Religion')['Students'].mean().reset_index()
    data_average = average_scores.to_dict(orient='records')

    return data_average