import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd
import os
import re

if 'table_displayed' not in st.session_state:
    st.session_state['table_displayed'] = False
    
if 'initialized' not in st.session_state:
    st.session_state['initialized'] = True
    st.session_state['image_path'] = "19_0927_plcy_real-id-license-ny.jpg"
    st.session_state['temp_path'] = "temp_image.jpg"
    st.session_state['df'] = pd.DataFrame()

st.title("ID Info Extraction Demo")

def extract_info_from_sample(text):
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

def extract_action():
    temp_path = "temp_image.jpg"
    extracted_text = pytesseract.image_to_string(temp_path)
    parsed_data = extract_info_from_sample(extracted_text)
    df = pd.DataFrame(list(parsed_data.items()), columns=['Field', 'Value'])
    table_placeholder.table(df)

    csv = df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="parsed_data.csv",
        mime="text/csv"
    )
    os.remove(temp_path)
    
example_image_path = "19_0927_plcy_real-id-license-ny.jpg"

if st.button("Upload Example Id"):
    image = Image.open(example_image_path)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    temp_path = "temp_image.jpg"
    image.save(temp_path)
    st.write("Extract Text From Image")

    if st.button("Extract", on_click=extract_action):
        pass