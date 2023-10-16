import streamlit as st
import hmac
import pandas as pd
import re
from dotenv import load_dotenv
load_dotenv()
import cloudinary
import cloudinary.uploader
import cloudinary.api

if "password" not in st.session_state:
    st.session_state.password = None

def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False
    if st.session_state.get("password_correct", False):
        return True
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


def get_annotated_text(result):
    ocr_text = result['info']['ocr']['adv_ocr']['data'][0]['textAnnotations'][0]['description']
    return ocr_text
    
def extract_id_information(result):
    ocr_text = result['info']['ocr']['adv_ocr']['data'][0]['textAnnotations'][0]['description']

    patterns = {
        "Full Name": r"MOTORIST\s*([A-Z\s,]+)",
        "Date of Birth": r"DOB (\d{1,2}/\d{1,2}/\d{4})",
        "Address": r"([\w\s]+), [A-Z]{2} \d{4,5}",  # Capture address in the format: "City Name, State ZipCode"
        "ID Number": r"ID (\d{2,3} \d{2,3} \d{2,3})",  # ID numbers of different lengths
        "Issue Date": r"Issued (\d{1,2}/\d{1,2}/\d{4})",
        "Expiry Date": r"Expires (\d{1,2}/\d{1,2}/\d{4})",
        "Gender": r"Sex (\w)",
        "Height": r"Height ([\d\'\-]+)"
    }

    extracted_data_list = []
    for label, pattern in patterns.items():
        match = re.search(pattern, ocr_text)
        extracted_value = match.group(1).strip() if match else None
        extracted_data_list.append({
            "Label": label,
            "Id Info": extracted_value,
            "regex pattern": pattern
        })

    address_parts = [item for item in extracted_data_list if item["Label"] == "Address"]
    if address_parts:
        address_parts = address_parts[0]["Id Info"].split("\n")
        if len(address_parts) > 1:
            refined_address = address_parts[-1]
        else:
            refined_address = address_parts[0]
        for item in extracted_data_list:
            if item["Label"] == "Address":
                item["Id Info"] = refined_address

    return extracted_data_list