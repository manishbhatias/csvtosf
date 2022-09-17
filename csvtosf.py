import sys, os
from PyInquirer import prompt
from sqlalchemy import create_engine, exc
from snowflake.sqlalchemy import URL
import pandas as pd

class csvtosf:
    # Configure Logging to console
    def __init__(self):
        try:
            self.connect()
            self.importcsv()
        finally:
            self.close()
    
    # Setup connection to Snowflake using sqlalchemy
    def connect(self):
        questions = [
            {
                'type': 'input',
                'name': 'user',
                'message': 'Username:'                
            },
            {
                'type': 'password',
                'name': 'password',
                'message': 'Password:'                
            },
            {
                'type': 'input',
                'name': 'account',
                'message': 'Account (Combination of Org ID & Account ID):',
            },
            {
                'type': 'input',
                'name': 'warehouse',
                'message': 'Warehouse:',                
            },
            {
                'type': 'input',
                'name': 'database',
                'message': 'Database:'                
            },
            {
                'type': 'input',
                'name': 'schema',
                'message': 'Schema:',                
                'default': 'public'
            }
        ]        
        try:
            credentials = prompt(questions)
            self.engine = create_engine(URL(
                account=credentials['account'], 
                user=credentials['user'], 
                password=credentials['password'],
                warehouse=credentials['warehouse'],
                database=credentials['database'],
                schema=credentials['schema'],
            ))
            self.connection = self.engine.connect()
        except KeyError:
            print("Missing values!")            
            sys.exit(1)    
        except exc.SQLAlchemyError as e:
            print("Failed to connect!")            
            sys.exit(1)    
            
    def importcsv(self):
        questions = [            
            {
                'type': 'input',
                'name': 'file',
                'message': 'Path to csv file:'
            }
        ]
        try:            
            answers = prompt(questions)                                
            ## Read the csv file using pandas
            df = pd.read_csv(answers['file'], sep=',')
            
            # Print the first five rows
            print('Priting the first five rows...')
            print(df.head(5))
            filename, file_extension = os.path.splitext(answers['file'])
            
            # Import the file into Snowflake, replace any existing data
            print('Importing the file in snowflake...')
            df.to_sql(filename.lower(), con=self.connection, index=False, if_exists='replace')
            print('Import complete.')
        except FileNotFoundError as e:
            print("Unable to read file!")            
            sys.exit(1)
        except exc.SQLAlchemyError as e:
            print("Failed to connect!")
            print(e)
            sys.exit(1)
            
    # Close the connection and release resources
    def close(self):
        if hasattr(self, 'engine'):
            self.connection.close()
            self.engine.dispose()    
        
if __name__ == '__main__':    
    csvtosf()