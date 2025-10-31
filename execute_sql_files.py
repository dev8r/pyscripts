import os
import pyodbc
from tabulate import tabulate

def execute_sql_files(directory):
  
    with pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};Trusted_Connection=yes;') as conn:
        cursor = conn.cursor()

        # Iterate over all files in the directory
        for filename in os.listdir(directory):
            if filename.endswith(".sql"):
                filepath = os.path.join(directory, filename)
                with open(filepath, 'r') as file:
                    sql_script = file.read()
                    try:
                        cursor.execute(sql_script)
                       # conn.commit()
                        print(f"Executed {filename} successfully.")
                        
                        # Fetch and print the results
                        if cursor.description:
                            #columns = [desc[0] for desc in cursor.description]
                            rows = cursor.fetchall()
                            #check row count
                            if len(rows) == 0:
                                print("No rows returned.")
                            else:
                                #columns = [desc[0] for desc in cursor.description]
                                #print(tabulate(rows, headers="keys", tablefmt='pipe'))
                                affected_rows = cursor.rowcount
                                print(f"{affected_rows} rows affected.")

                    except Exception as e:
                        print(f"Failed to execute {filename}: {e}")
#create a function which execute each script in the directory using sqlcmd
#and print the output to the console

def execute_sqlcmd_files(directory, server):
    for filename in os.listdir(directory):
        if filename.endswith(".sql"):
            filepath = os.path.join(directory, filename)
            command = f'sqlcmd -S {server} -i "{filepath}" -E'
            try:
                result = os.popen(command).read()
                print(f"Executed {filename} successfully.")
                print(result)
            except Exception as e:
                print(f"Failed to execute {filename}: {e}")
        print(f"Execute {filename} with command {command} successfully.")
database = 'master'
server = 'oflappdb02.stg.cardinalhealth.net'

# Example usage
execute_sqlcmd_files(r'C:\GitHub\Release Scripts', server)

# Example usage
#execute_sql_files(r'C:\GitHub\optifreight-database\Release Scripts\User Management\temp')
