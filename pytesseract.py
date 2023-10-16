import streamlit as st
from PIL import Image
import os
import re
import pandas as pd
from pytesseract_container import get_text_extraction, parse_with_reg_expressions,  check_password

# if not check_password():
#     st.stop()  # Do not continue if check_password is not True.

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
    
st.title("ID Info Extraction Demo")
example_image_path = "example_id.jpg"
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
    parsed_data_list = parse_with_reg_expressions(st.session_state.extracted_text)
    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame(parsed_data_list)
    os.remove(temp_path)
    
if st.session_state.extraction_occurrence == False and st.session_state.upload_occurrence == True:
    with st.form("extract_form"):
        extract = st.form_submit_button("Extract", on_click=extraction_callback)
        
if st.session_state.extraction_occurrence == True and st.session_state.data_form_occurrence == False:
    with st.form("data_form"):
        with st.sidebar:
            st.image(st.session_state.image, caption="Uploaded Image", use_column_width=True)
        st.markdown("***please edit your id information to match your id if needed.***")
        st.markdown("*To further validate the concept, note the regex value used to extract the information from the pytesseract ocr response*")
        st.data_editor(st.session_state.df,  hide_index = True, disabled = ["Label", "Regex Pattern"])
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
    st.markdown("""
                ### *This example demo is based on the use of a private, custom implementation of the `pytesseract` library*
                ### *To see an example of a third party integrative service integration that uses Google Vision as the ocr engine, click on the link below*.
                [**3rd Party OCR Example Link**](https://idextract.streamlit.app)
                """)
    
    reset_button = st.button("RESET DEMO")
    
    if reset_button:
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()