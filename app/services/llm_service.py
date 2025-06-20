# import openai
import pandas as pd
from dotenv import dotenv_values

def generate_sql_from_question(openai, question: str, table_schema: str = None, table_name: str = "data_pump") -> str:
    """
    Send the user question to the LLM for transforming to SQL.
    """
    system_prompt = (
        "You are a helpful assistant that generates SQLite SQL queries from natural language questions. "
        "The user will describe what they want to know about a database, and you should respond with only the SQL query. "
        "Do not include explanations. Use only standard SQLite 3 syntax. If the question is vague, make reasonable assumptions."
    )

    user_prompt = f"""
    Table Schema:
    {table_schema}

    Table Name:
    {table_name}

    Question: {question}
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        sql_query = response.choices[0].message.content.strip()

        if sql_query.startswith("```sql"):
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

        return sql_query

    except Exception as e:
        print(f"ERROR: Failed to generate SQL query: {e}")
        return "SELECT 'Failed to generate SQL due to an error.';"
    
def generate_sql_from_error(openai, error_msg: str):
    """
    Send the error message to the LLM for generarting correct SQL.
    """
    system_prompt = (
        "You are a helpful assistant that generates SQLite SQL queries from natural language questions. "
        "The user will describe what they want to know about a database, and you should respond with only the SQL query. "
        "Do not include explanations. Use only standard SQLite 3 syntax. If the question is vague, make reasonable assumptions."
    )

    user_prompt = f"Provide fixed version of sql query w.r.t. error message: {error_msg}"
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        sql_query = response.choices[0].message.content.strip()

        if sql_query.startswith("```sql"):
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

        return sql_query

    except Exception as e:
        print(f"ERROR: Failed to generate SQL query: {e}")
        return "SELECT 'Failed to generate SQL due to an error.';"


def analyze_dataframe_with_llm(openai, df: pd.DataFrame, user_question: str) -> str:
    """
    Send the query result + user question to the LLM for analysis.
    """
    # Convert DataFrame to CSV for concise representation
    csv_data = df.to_csv(index=False)

    system_prompt = (
        "You are a senior data analyst. The user will provide a question and some tabular data (CSV format). "
        "Give a concise, plain-English summary of insights relevant to their question. Be accurate and helpful."
    )

    user_input = f"""User Question:
        {user_question}

        CSV Data:
        {csv_data}
    """

    response = openai.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
        temperature=0.4,
    )

    return response.choices[0].message.content
