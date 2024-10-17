# climbing_routes_per_grade_with_tooltip.py

import pandas as pd
import plotly.express as px

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
    
    # Filter to include only successful ascents
    data = data[data['is_ascent'] == True]  # Only ascents

    # Convert 'date' column to datetime
    data['date'] = pd.to_datetime(data['date'])
    
    return data

def group_routes_per_week_and_grade(data):
    # Group by week and grade and count the number of routes for each grade in each week
    weekly_routes_per_grade = data.groupby([pd.Grouper(key='date', freq='W'), 'numeric_grade']).size().reset_index(name='route_count')
    
    # Add the grade label to show in the tooltip
    weekly_routes_per_grade['grade_label'] = weekly_routes_per_grade['numeric_grade'].map(grade_mapping_reverse)

    return weekly_routes_per_grade

def plot_routes_per_grade_to_html(weekly_routes_per_grade, html_output="routes_per_grade_with_tooltip.html"):
    # Create the Plotly chart to show the number of routes per grade per week
    fig = px.bar(
        weekly_routes_per_grade, 
        x='date', 
        y='route_count', 
        color='numeric_grade', 
        hover_data={'grade_label': True, 'numeric_grade': False},  # Show converted grade in tooltip
        title='Number of Routes per Grade per Week',
        labels={'route_count': 'Number of Routes', 'date': 'Week', 'numeric_grade': 'Climbing Grade'},
        color_continuous_scale=px.colors.sequential.Plasma
    )

    # Update y-axis tick labels to display climbing grades instead of numeric values
    fig.update_layout(
        yaxis_title="Number of Routes",
        xaxis_title="Week",
        coloraxis_colorbar=dict(
            title="Climbing Grade",
            tickvals=list(grade_mapping.values()),
            ticktext=list(grade_mapping_reverse.values())
        )
    )

    # Save plot as an HTML file
    fig.write_html(html_output)
    print(f"Chart saved as {html_output}")

if __name__ == "__main__":
    # File path for the dataset
    file_path = 'export.csv'  # Replace with the path to your dataset
    
    # Step 1: Load and prepare data
    data = load_and_prepare_data(file_path)
    
    # Step 2: Group data by week and grade, and count the number of routes
    weekly_routes_per_grade = group_routes_per_week_and_grade(data)
    
    # Step 3: Plot the chart and save it as an HTML file with tooltips showing the converted grade
    plot_routes_per_grade_to_html(weekly_routes_per_grade, html_output="routes_per_grade.html")