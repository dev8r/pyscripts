import csv

# Read the CSV file
with open('test.csv', mode='r') as file:
    reader = csv.reader(file)
    rows = list(reader)

# Rotate the data
rotated_data = zip(rows[0], rows[1])

# Write the rotated data to a new CSV file
with open('rotated_output.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Column Name', 'Value'])  # Header row
    writer.writerows(rotated_data)
