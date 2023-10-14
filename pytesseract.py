import streamlit as st
from PIL import Image
import os
import re
import pandas as pd
from pytesseract_container import get_text_extraction

extracted_text = get_text_extraction()

if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = extracted_text
if "upload_occurrence" not in st.session_state:
    st.session_state.upload_occurrence = False
if "extraction_occurrence" not in st.session_state:
    st.session_state.extraction_occurrence = False
if "data_form_occurrence" not in st.session_state:
    st.session_state.data_form_occurrence = False

def data_form_callback():
    st.session_state.data_form_occurrence = True
    
def extraction_callback():
    st.session_state.extraction_occurrence = True

def final_callback():
    st.session_state.data_form_occurrence = False
    st.session_state.extraction_occurrence = False
    
def parse_with_reg_expressions(text):
    data = {}
    name_match = re.search(r"MOTORIST\.\s*(?P<name>[A-Z\s,\.]+)\s*SAMPLE", text)
    if name_match:
        data["Full Name"] = name_match.group("name").replace(",", "").strip()
    address_match = re.search(r"(?P<address>\d+\s[A-Z\s]+)\s*,\s*NY\s*\d+", text)
    if address_match:
        data["Address"] = address_match.group("address").strip()
    sex_match = re.search(r"Sex\s*(?P<sex>[MF])", text)
    if sex_match:
        data["Sex"] = sex_match.group("sex")
    height_match = re.search(r"Height\s*(?P<height>\d+'-\d+\")", text)
    if height_match:
        data["Height"] = height_match.group("height")
    dob_match = re.search(r"(?P<dob>\d{2}/\d{2}/\d{4})", text)
    if dob_match:
        data["DOB"] = dob_match.group("dob")
    exp_match = re.search(r"Exes\s*(?P<exp>\d{2}/\d{2}/\d{4})", text)
    if exp_match:
        data["Expiration Date"] = exp_match.group("exp")

    issue_match = re.search(r"issued\s*(?P<issue>\d{2}/\d{2}/\d{4})", text)
    if issue_match:
        data["Issue Date"] = issue_match.group("issue")

    return data

st.title("ID Info Extraction Demo")

example_image_path = "example-id.jpg"

if "example_image_path" not in st.session_state:
    st.session_state.example_image_path = example_image_path

if st.button("Upload Example Id"):
    st.session_state.upload_occurrence = True
    image = Image.open(example_image_path)
    if "image" not in st.session_state:
        st.session_state.image = image
    temp_path = "temp_image.jpg"
    image.save(temp_path)
    st.image(st.session_state.image, caption="Uploaded Image", use_column_width=True)
    parsed_data = parse_with_reg_expressions(st.session_state.extracted_text)
    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame(list(parsed_data.items()), columns=['Field', 'Value'])
    os.remove(temp_path)
    
if st.session_state.extraction_occurrence == False and st.session_state.upload_occurrence == True:
    with st.form("extract_form"):
        
        extract = st.form_submit_button("Extract", on_click=extraction_callback)
        
if st.session_state.extraction_occurrence == True and st.session_state.data_form_occurrence == False:
    
    with st.form("data_form"):
        st.data_editor(st.session_state.df,  hide_index = True, )
        csv = st.session_state.df.to_csv(index=False)
        if "csv" not in st.session_state:
            st.session_state.csv = csv

        st.submit_button = st.form_submit_button("Confirm and Submit", on_click=data_form_callback)
    
if st.session_state.extraction_occurrence == True and st.session_state.data_form_occurrence == True:
    st.markdown("""
                ## Thank You For Submitting Your Id Info
                """)
    st.markdown("""
                ### Download A Copy For Your Records Below\n
                """)
    st.download_button(
        label = "Download CSV File and Reset Demo",
        data=st.session_state.csv,
        file_name = "example excel file / restart demo",
        mime="text/csv", key="download_button",
        on_click=final_callback()
    )