import sqlite3
import pandas as pd
from threading import Lock

class QueryExecutor(object):
    _instance = None
    _lock = Lock()

    def __new__(cls, path_to_db: str):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(QueryExecutor, cls).__new__(cls)
                cls._instance.__initialized = False
        return cls._instance

    def __init__(self, path_to_db: str):
        if self.__initialized:
            return

        self.path_to_db = path_to_db
        self.conn = self.__connect()
        self.__initialized = True

    def __connect(self):
        try:
            conn = sqlite3.connect(self.path_to_db, check_same_thread=False)
            return conn
        except sqlite3.Error as e:
            print(f"ERROR: Cannot connect db due to: {e}")
            return

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def run_query(self, query: str):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            rows = cursor.fetchall()
            cursor.close()
            return {"columns": columns, "rows": rows}
        
        except sqlite3.Error as e:
            print(f"ERROR: Failed to execute query: {e}")
            return
    
    def run_query_dataframe(self, query: str):
        try:
            return pd.read_sql_query(query, self.conn)
        except Exception as e:
            return pd.DataFrame({"error": [str(e)]})
        
