import streamlit as st
import hmac
import pandas as pd
import re
from dotenv import load_dotenv
load_dotenv()
import cloudinary
import cloudinary.uploader
import cloudinary.api

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

# extracted_data = cloudinary.uploader.upload("example_id.jpg", ocr = "adv_ocr")
# parsed_data = extract_id_information(st.session_state.extracted_data)
# df = pd.DataFrame([parsed_data])
# edited_data = st.data_editor(st.session_state.df,  hide_index=True)
# # in it's current configuration it resembles:
# current_outcome_markdown_table_example = """
# | Full Name | Date of Birth | Address | ID Number | Issue Date | Expiry Date | Gender | Height | 
# | MICHAEL, MATTHEW | 10/30/1972 | 2345 ANYWHERE STREET | 123 456 789 | 10/30/2017 | 10/30/2025 | M | 5'-08 |
# """
# # To show you what the OCR Model is returning, that we need to parse:
# text_for_parsing = st.write(get_annotated_text(st.session_state.extracted_data))
# # using an example Id we receive the following from the `ocr` response:
# # "`text_for_parsing` = TORM STAPLE 1400 SERIGALA NEW YORK STATE USA DRIVER LICENSE HE Class D SAMPLE STATE -Les ID 123 456 789 MOTORIST MICHAEL, MATTHEW 2345 ANYWHERE STREET YOUR CITY, NY 12345 Sex M Height 5'-08" Eyes BRO DOB 10/30/1972 Expires 10/30/2025 E NONE Michael Matthew Motorist & NONE OCT 72 R Issued 10/30/2017 **1982 MICHAEL EXCELSIO Organ Donor"
# desired_outcome_markdown_table_example = """
#                                 |Label | Id Info | regex pattern |
#                                 |:-----|:--------|:--------------|
#                                 |Full Name | MICHAEL, MATTHEW | ([A-Z\s,]+) |
#                                 | Data of Birth | 10/30/1972 | (\d{2}\/\d{2}\/\d{4})|
#                                 | Address | etc... | etc...|
#                                 """
# # How can I adjust my script so the the dataframe is generated looks like the desired outcome?
# # How can I make the regex work with more examples of Id's, not just the one example-id?

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password2"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False
