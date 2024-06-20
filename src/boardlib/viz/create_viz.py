
import pandas as pd

# Read the CSV data
csv_file = r'/home/ptschaikner/coding/Tension/test.csv'  # Update this with the actual path to your CSV file
data = pd.read_csv(csv_file)

# Convert the data to JSON format for embedding in the HTML
data_json = data.to_json(orient='records')

# Read the HTML template
with open('template.html', 'r') as file:
    html_template = file.read()

# Replace the placeholder with the actual data
html_content = html_template.replace('__DATA__', data_json)

# Write the final HTML to a file
output_file = 'scatterplot.html'
with open(output_file, 'w') as file:
    file.write(html_content)

print(f"HTML file '{output_file}' has been created.")
