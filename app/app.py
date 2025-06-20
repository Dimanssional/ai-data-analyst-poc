import os
import openai
import streamlit as st

from services.llm_service import *
from services.query_executor import QueryExecutor
from db.db import *

from dotenv import dotenv_values

config = dotenv_values("/app/.env")

API_KEY = config["API_KEY"]

openai.api_key = API_KEY
# Constants
PATH_TO_DB = config["PATH_TO_DB"]
PATH_TO_DATA = config["PATH_TO_DATA"]

RETRY_LIMIT = 3
TABLE_SCHEMA = get_table_schema(PATH_TO_DATA)
TABLE_NAME = "data_pump"

# Streamlit page setup
st.set_page_config(page_title="AI Data Analyst", layout="centered")
st.title("🤖 AI Data Analyst Demo")
st.caption("Upload Excel → Ask Data Questions → Get SQL Results")

if not os.path.exists(PATH_TO_DB):
    create_sqlitedb(PATH_TO_DB)
    xlsx_to_sqlitedb(PATH_TO_DB, PATH_TO_DATA, TABLE_NAME)

# Query executor instance
db_conn = QueryExecutor(PATH_TO_DB)

# Question input
user_question = st.text_input("Ask a question about the data:")

if user_question:
    with st.spinner("Analyzing..."):
        sql_query = generate_sql_from_question(openai, user_question, table_schema=TABLE_SCHEMA, table_name=TABLE_NAME)
        st.code(sql_query, language="sql")

        for attempt in range(RETRY_LIMIT):
            result_df = db_conn.run_query_dataframe(sql_query)

            if "error" not in result_df.columns:
                break  # Success
            else:
                error_message = result_df["error"][0]
                st.warning(f"Attempt {attempt+1} failed with error:\n{error_message}")
                sql_query = generate_sql_from_error(openai, error_message)
                st.code(sql_query, language="sql")
        else:
            st.error("All attempts to fix the query failed.")

        st.write("Result:")
        st.dataframe(result_df)

        # AI analysis
        st.subheader("AI Interpretation")
        insights = analyze_dataframe_with_llm(openai, result_df, user_question)
        st.markdown(insights)

        # Just optional visualization. Not accurate, because of MVP
        st.bar_chart(result_df)
        st.line_chart(result_df)

