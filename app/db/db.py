import os
import sqlite3
import pandas as pd

PATH_TO_DB = "/Users/dmla/Projects/TrainingFolder/ai-data-analyst-poc/app/db/my_db.db"
PATH_TO_DATA = "/Users/dmla/Projects/TrainingFolder/ai-data-analyst-poc/app/db/data/Data_Dump.xlsx"

def create_sqlitedb(path_to_db: str):
    os.makedirs(os.path.dirname(path_to_db), exist_ok=True)

def get_table_schema(path_to_data: str, sheet_name: str = "Sheet1") -> str:
    input_df = pd.read_excel(path_to_data, sheet_name=sheet_name)
    input_df.rename(columns={"Unnamed: 0": "ID"}, inplace=True)
    return "\n".join([f"{col}: {dtype}" for col, dtype in zip(input_df.columns, input_df.dtypes)])

def xlsx_to_sqlitedb(path_to_db: str, path_to_data: str, table_name: str = "data_pump", sheet_name: str = "Sheet1"):

    input_df = pd.read_excel(path_to_data, sheet_name=sheet_name)
    input_df.rename(columns={"Unnamed: 0": "ID"}, inplace=True)
    conn = sqlite3.connect(path_to_db)

    input_df.to_sql(table_name, conn, if_exists="replace", index=False)

    print(f"SUCCES: Data from '{path_to_data}' written to '{path_to_db}' in table '{table_name}'")

    conn.close()


# if __name__ == "__main__":

#     create_sqlitedb(PATH_TO_DB)
#     print(get_table_schema(PATH_TO_DATA))
#     xlsx_to_sqlitedb(PATH_TO_DB, PATH_TO_DATA)

