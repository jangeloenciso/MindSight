import numpy as np
import plotly.express as px
import pandas as pd

# Reading the tips.csv file
data = pd.read_csv('collegesum.csv')

# for pie chart
# fig = px.pie(data, names='Gender', 
#              height=300, width=600, 
#              title='IDENTITY',
#              color_discrete_sequence=['#DB9050', '#095371', '#6092C0'])

# for bar graph
# fig = px.bar(data, x=data['Colleges'], y=data['Students'], title='COLLEGE SUMMARIES', color_discrete_sequence =['#095371'])

fig.show()
