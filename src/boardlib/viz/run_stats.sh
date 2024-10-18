#!/bin/bash
# Check if db.sqlite3 exists and get it if not
if [ ! -f "db.sqlite3" ]; then
    echo "Downloading db.sqlite3 file."
    boardlib database tension db.sqlite3
fi

if [ -f "db.sqlite3" ]; then
    echo "Found a valid db.sqlite3 file."
fi

# Prompt for username
read -p "Enter your username: " username

# Check if export.csv exists and ask user if they want to update it
if [ -f "export.csv" ]; then
    read -p "An existing export.csv file exists. Do you want to update it from Tension Server? (Y/N): " update_choice
    case $update_choice in
        Y|y)
            echo "Updating existing export.csv file."
            rm export.csv
            # Run the boardlib command with the provided username
            boardlib logbook tension --username="$username" --output=export.csv --grade-type=font --database=db.sqlite3

            # Check if export.csv was created successfully
            if [ ! -f "export.csv" ]; then
                echo "Error: export.csv was not created. Please check the boardlib command."
                exit 1
            fi

            ;;
        N|n)
            echo "Keeping the existing export.csv file."
            ;;
        *)
            echo "Invalid choice. Please enter Y or N."
            ;;
    esac
fi


# Remove .html files in the folder if they exist
for file in *.html; do
    if [ -f "$file" ]; then
        echo "Removing $file"
        rm "$file"
    fi
done

# Run the Python scripts
python3 climbing_grade.py
python3 routes_per_grade.py

# Open the generated HTML files in the folder
for file in routes_per_grade.html; do
    if [ -f "$file" ]; then
        echo "Opening $file"
        open "$file"
    fi
done

# Open the generated HTML files in the folder
for file in climbing_grades.html; do
    if [ -f "$file" ]; then
        echo "Opening $file"
        open "$file"
    fi
done

