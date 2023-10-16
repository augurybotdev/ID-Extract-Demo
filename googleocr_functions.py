import streamlit as st
import hmac
import re

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


def extract_id_information(result):
    ocr_text = result['info']['ocr']['adv_ocr']['data'][0]['textAnnotations'][0]['description']
    patterns = {
        "Full Name": r"MOTORIST\n([A-Z\s,]+)",
        "Date of Birth": r"DOB (\d{2}/\d{2}/\d{4})",
        "Address": r"([\w\s]+)\nYOUR CITY, NY",
        "ID Number": r"ID (\d{3} \d{3} \d{3})",
        "Issue Date": r"Issued (\d{2}/\d{2}/\d{4})",
        "Expiry Date": r"Expires (\d{2}/\d{2}/\d{4})",
        "Gender": r"Sex (\w)",
        "Height": r"Height ([\d\'\-]+)"
    }
    extracted_data = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, ocr_text)
        extracted_data[field] = match.group(1).strip() if match else None
    address_parts = extracted_data["Address"].split("\n")
    if len(address_parts) > 1:
        refined_address = address_parts[-1]
    else:
        refined_address = extracted_data["Address"]
    extracted_data["Address"] = refined_address
    return extracted_data