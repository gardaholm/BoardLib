# climbing_chart_html.py

import pandas as pd
import plotly.graph_objects as go

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

def group_by_week(data):
    # Filter data by ascents (True or False)
    ascent_true = data[data['is_ascent'] == True]
    ascent_false = data[data['is_ascent'] == False]

    # Group by week and calculate stats
    weekly_stats_true = ascent_true.groupby(pd.Grouper(key='date', freq='W')).agg(
        avg_grade=('numeric_grade', 'mean'),
        min_grade=('numeric_grade', 'min'),
        max_grade=('numeric_grade', 'max')
    ).dropna()

    weekly_stats_false = ascent_false.groupby(pd.Grouper(key='date', freq='W')).agg(
        avg_grade=('numeric_grade', 'mean'),
        min_grade=('numeric_grade', 'min'),
        max_grade=('numeric_grade', 'max')
    ).dropna()
    
    return weekly_stats_true, weekly_stats_false

def plot_grades_to_html(weekly_stats_true, weekly_stats_false, html_output="climbing_grades.html"):
    # Create traces for ascents (True) and non-ascents (False)
    fig = go.Figure()

    # Ascents (True) trace with error bars for min and max
    fig.add_trace(go.Scatter(
        x=weekly_stats_true.index,
        y=weekly_stats_true['avg_grade'],
        error_y=dict(
            type='data',
            symmetric=False,
            array=weekly_stats_true['max_grade'] - weekly_stats_true['avg_grade'],
            arrayminus=weekly_stats_true['avg_grade'] - weekly_stats_true['min_grade']
        ),
        mode='markers',
        marker=dict(color='blue'),
        name='Ascents'
    ))

    # Non-ascents (False) trace with error bars for min and max
    fig.add_trace(go.Scatter(
        x=weekly_stats_false.index,
        y=weekly_stats_false['avg_grade'],
        error_y=dict(
            type='data',
            symmetric=False,
            array=weekly_stats_false['max_grade'] - weekly_stats_false['avg_grade'],
            arrayminus=weekly_stats_false['avg_grade'] - weekly_stats_false['min_grade']
        ),
        mode='markers',
        marker=dict(color='red'),
        name='Non-Ascents'
    ))

    # Customize layout
    fig.update_layout(
        title='Weekly Average, Min, and Max Climbing Grades (Ascents vs Non-Ascents)',
        xaxis_title='Week',
        yaxis_title='Climbing Grade',
        yaxis=dict(
            tickvals=list(grade_mapping.values()),
            ticktext=list(grade_mapping_reverse.values())
        ),
        legend_title="Climb Type"
    )

    # Save plot as an HTML file
    fig.write_html(html_output)
    print(f"Chart saved as {html_output}")

if __name__ == "__main__":
    # File path for the dataset
    file_path = 'export.csv'  # Replace with the path to your dataset
    
    # Step 1: Load and prepare data
    data = load_and_prepare_data(file_path)
    
    # Step 2: Group data by week and calculate min, max, and average grades
    weekly_stats_true, weekly_stats_false = group_by_week(data)
    
    # Step 3: Plot the chart and save it as an HTML file
    plot_grades_to_html(weekly_stats_true, weekly_stats_false, html_output="climbing_grades.html")