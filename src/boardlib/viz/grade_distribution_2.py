# climbing_routes_per_grade_with_date_filter.py

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Define grade mapping
grade_mapping = {
    '4a': 10, '4b': 11, '4c': 12, '5a': 13, '5b': 14, '5c': 15,
    '6a': 16, '6a+': 17, '6b': 18, '6b+': 19, '6c': 20, '6c+': 21,
    '7a': 22, '7a+': 23, '7b': 24, '7b+': 25, '7c': 26, '7c+': 27,
    '8a': 28, '8a+': 29, '8b': 30, '8b+': 31, '8c': 32, '8c+': 33
}
grade_mapping_reverse = {v: k for k, v in grade_mapping.items()}

def load_and_prepare_data(file_path):
    # Load dataset
    data = pd.read_csv(file_path)
    
    # Combine 'logged_grade' and 'displayed_grade'
    data['grade_combined'] = data['logged_grade'].fillna(data['displayed_grade'])
    
    # Map grades to numeric values
    data['numeric_grade'] = data['grade_combined'].map(grade_mapping)
    
    # Convert 'date' column to datetime
    data['date'] = pd.to_datetime(data['date'])
    
    return data

def group_routes_by_grade_and_ascent(data):
    # Group by grade and ascent status, and count the number of routes
    grouped_data = data.groupby(['grade_combined', 'is_ascent']).size().reset_index(name='count')
    
    return grouped_data

# Initialize Dash app
app = Dash(__name__)

# Load data
file_path = 'export.csv'  # Replace with your dataset
df = load_and_prepare_data(file_path)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Interactive Climbing Chart with Timeframe Filter"),
    
    # Date range picker
    dcc.DatePickerRange(
        id='date-picker',
        min_date_allowed=df['date'].min(),
        max_date_allowed=df['date'].max(),
        start_date=df['date'].min(),
        end_date=df['date'].max()
    ),
    
    # Graph output
    dcc.Graph(id='climbing-chart'),
])

# Callback to update the graph based on the selected date range
@app.callback(
    Output('climbing-chart', 'figure'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')
)
def update_chart(start_date, end_date):
    # Filter data based on the selected date range
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    # Group data by grade and ascent status within the selected date range
    grouped_data = filtered_df.groupby(['grade_combined', 'is_ascent']).size().reset_index(name='count')
    
    # Create the Plotly chart with grades on x-axis, count on y-axis, and differentiated by ascent status
    fig = px.bar(
        grouped_data, 
        x='grade_combined', 
        y='count', 
        color='is_ascent', 
        title='Number of Routes per Grade (Differentiated by Ascent Status)',
        labels={'grade_combined': 'Climbing Grade', 'count': 'Number of Routes', 'is_ascent': 'Ascent Status'},
        barmode='group'
    )
    
    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)