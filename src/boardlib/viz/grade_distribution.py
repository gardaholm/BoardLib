# climbing_routes_per_grade_with_ascent.py

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
    
    return data

def group_routes_by_grade_and_ascent(data):
    # Group by grade and ascent status, and count the number of routes
    grouped_data = data.groupby(['grade_combined', 'is_ascent']).size().reset_index(name='count')
    
    return grouped_data

def plot_routes_by_grade_to_html(grouped_data, html_output="routes_by_grade.html"):
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

    # Save plot as an HTML file
    fig.write_html(html_output)
    print(f"Chart saved as {html_output}")

if __name__ == "__main__":
    # File path for the dataset
    file_path = 'export.csv'  # Replace with the path to your dataset
    
    # Step 1: Load and prepare data
    data = load_and_prepare_data(file_path)
    
    # Step 2: Group data by grade and ascent status, and count the number of routes
    grouped_data = group_routes_by_grade_and_ascent(data)
    
    # Step 3: Plot the chart and save it as an HTML file
    plot_routes_by_grade_to_html(grouped_data, html_output="routes_by_grade.html")