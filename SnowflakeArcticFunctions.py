from snowflake.snowpark import Session
from snowflake.cortex import Complete

connection_parameters = {
    "account": "zssxobc-icb91550",
    "user": "mrudhulahacks",
    "password": "Akhil@1993$"
    }  
session = Session.builder.configs(connection_parameters).getOrCreate()

def get_response_old(prompt):
    response = Complete('gemma-7b', prompt)
    return response

def get_response(prompt):
    prompt = prompt.replace("'", "\\'")
    # prompt = f"Summarize this transcript in less than 200 words. Put the product name, defect if any, and summary in JSON format: {entered_text}"
    cortex_prompt = "'[INST] " + prompt + " [/INST]'"
    cortex_response = session.sql(f"select snowflake.cortex.complete('snowflake-arctic', {cortex_prompt}) as response").to_pandas().iloc[0]['RESPONSE']
    return cortex_response
    # st.json(cortex_response)
           