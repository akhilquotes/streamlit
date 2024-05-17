import streamlit as st
import utilities as utilities
import os
from dotenv import load_dotenv
from st_ant_tree import st_ant_tree
from streamlit_tree_select import tree_select
import SnowflakeArcticFunctions as saf 
import re 
import json
import extra_streamlit_components as stx

load_dotenv()

st.set_page_config(layout='wide',page_title="Contract Highlights", page_icon="📈")
st.title("Timeline")
files_list = utilities.get_files_list()
# return_select = tree_select(files_list)



selected_file = st_ant_tree(files_list,treeCheckable=False,multiple=False)
st.sidebar.write(selected_file)

text = utilities.load_pdf('Files/Authorized Google Reseller Agreement/Authorized Google Reseller Agreement.pdf')
st.write(text[:200])
# timeline_prompt = f"""
#     Provide all timeline or duration information from given text in form of json array with keys like Timestamp, EventType, EventDescription
#     in descending order of Timestamp. Using provided details, give approximate date for each Event and add every possible detail regarding Event in EventDescription.
#     Make sure to include all possible details : {text} """
prompt=f"Provide all dates and corresponding event details from given contract. Put the Timestamp, EventType, EventDescription in JSON format: {text}"
response = saf.get_response(prompt)
st.write(response)
# with st.spinner('Wait for it...'):
#     text = utilities.load_pdf('Files/'+selected_file)
#     timeline_prompt = """
#         Provide all timeline or duration information from given text in form of json array with keys like Timestamp, EventType, EventDescription
#         in descending order of Timestamp. Using provided details, give approximate date for each Event and add every possible detail regarding Event in EventDescription.
#         Make sure to include all possible details
#     """+text
#     response = saf.get_response(timeline_prompt)
#     timeline_json = re.search(r'\[([^}]+)\]', response).group(0)
#     timeline = json.loads(timeline_json)

#     chosen_id = stx.tab_bar(data=[
#         stx.TabBarItemData(id=1, title="ToDo", description="Tasks to take care of"),
#         stx.TabBarItemData(id=2, title="Done", description="Tasks taken care of"),
#         stx.TabBarItemData(id=3, title="Overdue", description="Tasks missed out"),
#     ], default=1)
#     st.info(f"{chosen_id=}")
#     image_urls = ["https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.svg",
#                 "https://streamlit.io/images/brand/streamlit-logo-secondary-lightmark-lighttext.png",
#                 "https://ruslanmv.com/assets/images/posts/2020-10-17-Web-Application-Classification/streamlit_logo.png", ]
#     stx.bouncing_image(image_source=image_urls[int(chosen_id) - 1], animate=True, animation_time=1500, height=200, width=600)
#     time.sleep(5)
# 
# st.write(return_select)