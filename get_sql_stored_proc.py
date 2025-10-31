import pyodbc

def get_stored_procedure_dependencies_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    # Use regex to find all EXEC statements
    pattern = re.compile(r'\bEXEC\s+(\w+)', re.IGNORECASE)
    return pattern.findall(content)

def get_stored_procedure_dependencies(cursor, procedure_name):
    query = f"""
    SELECT DISTINCT referenced_entity_name
    FROM sys.dm_sql_referenced_entities ('dbo.{procedure_name}', 'OBJECT')
    WHERE referenced_class_desc = 'OBJECT_OR_COLUMN'
    AND referenced_minor_id = 0
    """
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]

def get_stored_procedure_definition(cursor, procedure_name):
    query = f"""
    SELECT OBJECT_DEFINITION (OBJECT_ID(N'dbo.{procedure_name}'))
    """
    cursor.execute(query)
    return cursor.fetchone()[0]

def download_stored_procedures(server, database, username, password, initial_procedure_file):
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        
        # Read the initial stored procedure name from the file
        with open(initial_procedure_file, 'r') as file:
            procedure_name = file.read().strip()
        
        # Get the main stored procedure definition
        main_procedure_definition = get_stored_procedure_definition(cursor, procedure_name)
        with open(f'{procedure_name}.sql', 'w') as file:
            file.write(main_procedure_definition)
        
        # Get dependent stored procedures
        dependencies = get_stored_procedure_dependencies(cursor, procedure_name)
        for dep in dependencies:
            dep_definition = get_stored_procedure_definition(cursor, dep)
            with open(f'{dep}.sql', 'w') as file:
                file.write(dep_definition)

def download_stored_procedures_IS(server, database, initial_procedure_file):
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        
        # Read the initial stored procedure name from the file
        with open(initial_procedure_file, 'r') as file:
            procedure_name = file.read().strip()
        
        # Get the main stored procedure definition
        main_procedure_definition = get_stored_procedure_definition(cursor, procedure_name)
        with open(f'{procedure_name}.sql', 'w') as file:
            file.write(main_procedure_definition)
        
        # Get dependent stored procedures
        dependencies = get_stored_procedure_dependencies(cursor, procedure_name)
        for dep in dependencies:
            dep_definition = get_stored_procedure_definition(cursor, dep)
            with open(f'{dep}.sql', 'w') as file:
                file.write(dep_definition)

# Example usage
server = 'db_server'
database = 'db_name'
username = 'your_username'
password = 'your_password'
initial_procedure_file = 'path_to_sql_file'

#download_stored_procedures(server, database, username, password, initial_procedure_file)
download_stored_procedures_IS(server, database, initial_procedure_file)
