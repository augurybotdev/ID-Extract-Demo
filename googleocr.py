import streamlit as st
import re
import os
import pandas as pd
from PIL import Image
import json
from googleocr_functions import check_password, extract_id_information, get_annotated_text
import cloudinary
import cloudinary.uploader
import cloudinary.api

api_key = st.secrets["cloudinary"]["api_key"]
api_secret = st.secrets["cloudinary"]["api_secret"]
cloud_name = st.secrets["cloudinary"]["cloud_name"]
CLOUDINARY_URL = f"cloudinary://{api_key}:{api_secret}@{cloud_name}"
os.environ["CLOUDINARY_URL"] = CLOUDINARY_URL

config = cloudinary.config(
    cloud_name = st.secrets["cloudinary"]["cloud_name"],
    api_key = st.secrets["cloudinary"]["api_key"],
    api_secret = st.secrets["cloudinary"]["api_secret"],
    secure = True
)
# st.markdown("### This Web App is Down For Maintenance.\n\nyou can see the demo for the localized bespoke version using `pytesseract` [HERE](https://idextract.streamlit.app)")

if not check_password():
    st.stop()  # Do not continue if check_password is not True.


def data_form_callback():
    st.session_state.data_form_occurrence = True 
def extraction_callback():
    st.session_state.extraction_occurrence = True
def final_callback():
    st.session_state.start_occurrence = False
    st.session_state.upload_occurrence = False
if "start_occurrence" not in st.session_state:
    st.session_state.start_occurrence = False
if "upload_occurrence" not in st.session_state:
    st.session_state.upload_occurrence = False
if "extraction_occurrence" not in st.session_state:
    st.session_state.extraction_occurrence = False
if "data_form_occurrence" not in st.session_state:
    st.session_state.data_form_occurrence = False
if "csv" not in st.session_state:
    st.session_state.csv = None
if "excel" not in st.session_state:
    st.session_state.excel = None
if "json" not in st.session_state:
    st.session_state.json = None

st.title("ID Info Extraction Demo")

if st.button("Upload Example Id"):
    example_image = "new_york_id.jpg"
    temp_path = "temp_path.jpg"
    image = Image.open('new_york_id.jpg')
    image.save(temp_path)
    
    if "example_image" not in st.session_state:
        st.session_state.example_image = example_image
        
    extracted_data = cloudinary.uploader.upload("new_york_id.jpg", ocr = "adv_ocr")
    if "extracted_data" not in st.session_state:
        st.session_state.extracted_data = extracted_data

    full_json_output = json.dumps(extracted_data, indent=4)
    if "json_output" not in st.session_state:
        st.session_state.json_output = full_json_output

    parsed_data = extract_id_information(extracted_data)
    if "parsed_data" not in st.session_state:
        st.session_state.parsed_data = parsed_data

    df = pd.DataFrame(parsed_data)
    if "df" not in st.session_state:
        st.session_state.df = df

    csv = st.session_state.df.to_csv(index=False)
    if "csv" not in st.session_state:
        st.session_state.csv = csv

    excel = st.session_state.df.to_excel('id_data.xlsx', index=False)
    if "excel" not in st.session_state:
            st.session_state.excel = excel
            
    output_json = json.dumps(parsed_data, indent=4)
    st.image(st.session_state.example_image, caption="uploaded identification", use_column_width=True)
    st.session_state.upload_occurrence = True
    os.remove(temp_path)    
    
if st.session_state.extraction_occurrence == False and st.session_state.upload_occurrence == True:
    with st.form("extract_form"):
        extraction_occurrence = st.form_submit_button("Extract", on_click=extraction_callback)
        
if st.session_state.extraction_occurrence == True and st.session_state.data_form_occurrence == False:
    with st.form("data_form"):
        st.markdown("""\
                    \n### ***!IMPORTANT!*** 
                    \n\n***your information must match the information on your ID***
                    \n\n*please ensure this information matches exactly with the information shown on your ID.*
                    """)
        with st.sidebar:
            st.image(st.session_state.example_image, caption="uploaded ID",width=None)
            unparsed_text_expander = st.expander("unparsed text")
            with unparsed_text_expander:
                st.write(get_annotated_text(st.session_state.extracted_data))
                
        edited_data = st.data_editor(st.session_state.df,  hide_index=True)
        if "edited_data" not in st.session_state:
            st.session_state.edited_data = edited_data
            
        submit_button = st.form_submit_button("Confirm and Submit", on_click=data_form_callback)
        
if st.session_state.extraction_occurrence == True and st.session_state.data_form_occurrence == True:
    st.markdown("""## **Thanks For Submitting Your Info For Testing!**\n---\n""")
    st.markdown("""### You can download a copy of your data as a JSON file, CSV file, or Excel file.\n""")
    space = st.empty()
    
    with space.container():
        st.write("    ")
    col1, col2, col4 = st.columns([1,1,1])
    
    with col2:
        with st.container():
            placeholder1 = st.empty()
            
        with st.container():
            placeholder2 = st.empty()
            
        with st.container():
            placeholder3 = st.empty()
            
        with st.container():
            placeholder4 = st.empty()
            
    with col1:        
        colsb1 = st.empty()
        cb1 = colsb1.checkbox("csv")
        colsb2 = st.empty()
        cb2 = colsb2.checkbox("excel")
        colsb3 = st.empty()
        cb3 = colsb3.checkbox("json")
        
    with col4:
        
        with st.container():
            holder1 = st.empty()
            holder2 = st.empty()
            holder3 = st.empty()
            holder4 = st.empty()
            
        if cb1:
            placeholder1.download_button(
                label = "csv download",
                data = "st.session_state.csv",
                file_name = "id_info.csv",
                mime="text/csv", key="download_button",
            )
            
        if cb2:
            placeholder2.download_button(
                label = "excel download",
                data = "st.session_state.excel",
                file_name = "id_info.xlsx",
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key="download_button2",
            )
            
        if cb3:
            placeholder3.download_button(
                label = "json download",
                data = "st.session_state.output_json",
                file_name = "id_info.json",
                mime = "application/json", key="download_button3",
            )
            
    reset_button = placeholder4.button("RESET DEMO", on_click=final_callback)
    
    if reset_button:
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()