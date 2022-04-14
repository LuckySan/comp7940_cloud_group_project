import pyodbc 
import yaml 
import sys
from dotenv import load_dotenv
load_dotenv()
import os



class SQLConnection(object): 

    # When the object is created it loads the environment variabes and stores them 
    def __init__(self):
        self.server=os.environ['SERVER']
        self.database=os.environ['DATABASE']
        self.uid=os.environ['UID']
        self.password=os.environ['PASSWORD']
        self.connector=None
        self.cursor = None


    @property
    def connection(self):
        return self._cnxn

    @property
    def cursor(self):
        return self._cursor

    def __enter__(self):

        print('connecting to MSSQL database...')
        self.connector = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.uid+';PWD='+self.password)
        self.cursor = self.connector.cursor()
        
        return self

    # Close the connection
    def __exit__(self, exc_type, exc_val, exc_tb):
        # If there is no error: commit the changes
        if exc_tb is None:
            self.connector.commit()
        else:
            self.connector.rollback()
        self.connector.close()




## Examples for usage with pandas 
# import pandas as pd
# with oracle_connection() as conn:
#     data =  pd.read_sql(sql, conn.connector)
 