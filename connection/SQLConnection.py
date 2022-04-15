from dotenv import load_dotenv
load_dotenv()
import os
import mysql.connector


class SQLConnection(object): 
    """
    1. This is the SQLConnection-Class -> It will take care of connecting to the database 
    For the object to work you need to create a .env file with the following credentials: 
    - Server: Host Address of the server 
    - UID: Username of the database
    - Database: Name of the database
    - Password: Password 

    2. The database object will take care of opening and closing the connection. If no error occurs it will commit the changes automatically to the database 

    Returns:
        _type_: _description_
    """

    # When the object is created it loads the environment variabes and stores them 
    def __init__(self):
        self.server=os.environ['SERVER']
        self.database=os.environ['DATABASE']
        self.uid=os.environ['UID']
        self.password=os.environ['PASSWORD']
        # self.connector=None
        # self.cursor = None


    @property
    def connector(self):
        return self._connector

    @connector.setter 
    def connector(self, value): 
        print("setting")
        self._connector = value

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, value):
        print("settting")
        self._cursor=value

    def __enter__(self):

        print('connecting to MSSQL database...')
        self._connector = mysql.connector.connect(
        host=self.server,
        user=self.uid,
        password=self.password, 
        database=self.database
        )

        self._cursor = self.connector.cursor()
        
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
# with SQLConnection() as conn:
#     sql="Select Count(*) FROM Dishes"
#     data =  pd.read_sql(sql, conn.connector)
#     print(data)
 