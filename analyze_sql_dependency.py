import re
import os
import sys
import pyodbc
import tkinter as tk
from tkinter import filedialog

def get_stored_procedure_dependencies_from_content (content):
    # Regular expression to match the pattern and capture the database, schema, and stored procedure name
    #pattern = re.compile(r'EXEC\s+(.*?)\.(.*?)\.(.*)', re.IGNORECASE)
    pattern = re.compile(r'EXEC\s+(\S+)', re.IGNORECASE)
    my_list = []
    # Find all matches
    matches = pattern.findall(content)

    for match in matches:
        procedure = match
        full_name = f"{procedure}"
        print(full_name)
        my_list.append(full_name)

    return my_list

def download_stored_procedures(cursor, initial_procedure_file, option, tempfilepath):        
        # Read the initial stored procedure name from the file
        with open(initial_procedure_file, 'r') as file:
            procedure_name = file.read().strip()
                
        # Get dependent stored procedures from the file
        dependencies = get_stored_procedure_dependencies_from_content(procedure_name)

        for dep in dependencies:
            full_name = dep.strip()
                
            if  option == '1' :
                print(full_name)
            else:
                dep_definition = get_stored_procedure_definition_obj_def(cursor, full_name)            
                filepath = tempfilepath + f'{full_name}.sql'
                with open(filepath, 'w') as file:
                    file.write(dep_definition)
                download_stored_procedures(cursor, filepath, option, tempfilepath)

def resolve_option(option, initial_procedure_file, tempfilepath):
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        if option == '2' :
            print(get_stored_procedure_definition(cursor, initial_procedure_file))
        else:
           download_stored_procedures(cursor, initial_procedure_file, option, tempfilepath)

def get_stored_procedure_definition(cursor, initial_procedure_file):
    stored_procedure_name = get_file_component(initial_procedure_file)
    cursor.execute(f"EXEC sp_helptext '{stored_procedure_name}'")
    sp_helptext_results = [row[0] for row in cursor.fetchall()]
    return ''.join(sp_helptext_results)

def get_stored_procedure_definition_obj_def(cursor, procedure_name):
    query = f"""
    SELECT OBJECT_DEFINITION (OBJECT_ID(N'{procedure_name}'))
    """
    print(query)
    cursor.execute(query)
    return cursor.fetchone()[0]

def get_file_component(directory_path):
    return os.path.basename(directory_path)

def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename()
    return file_path

def select_folder():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_selected = filedialog.askdirectory(title="Select output folder:") 
    folder_selected = folder_selected + "/"
    print("Selected folder:", folder_selected)
    return folder_selected
    

server = 'db_server'
database = 'db_name'
tempfilepath = select_folder()
input_initial_proc_file  = select_file()
print(f"Selected file: {input_initial_proc_file}")
input_option = input(
'''
What would you like to do 
(0) Default behavior download SP and referenced SPs
(1) print dependent SP
(2) show SP definition include [] around sp name
>>''')
print(input_option)
resolve_option(input_option, input_initial_proc_file, tempfilepath)
