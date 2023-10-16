# import pytesseract
import streamlit as st
import hmac
import re

def get_text_extraction():
    predefined_text = """\
    YORK STATE™ 3 |\
    IVER LICENSE\
    0123 456 789 ous D MOTORIST. MICHAEL, MATTHEW. SAMPLE\
    2345 ANYWHERE STREET YOUR CITY, NY 12345\
    Sex M_ Height 5'-08" Ges BRO 008 10/30/1972 Exes 10/30/2025. NONE\
    R NONE\
    'issued 10/30/2017\
    """
    return predefined_text

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

def parse_with_reg_expressions(text):
    regex_patterns = {
        "Full Name": r"MOTORIST\.\s*(?P<name>[A-Z\s,\.]+)\s*SAMPLE",
        "Address": r"(?P<address>\d+\s[A-Z\s]+)\s*,\s*NY\s*\d+",
        "Sex": r"Sex\s*(?P<sex>[MF])",
        "Height": r"Height\s*(?P<height>\d+'-\d+\")",
        "DOB": r"(?P<dob>\d{2}/\d{2}/\d{4})",
        "Expiration Date": r"Exes\s*(?P<exp>\d{2}/\d{2}/\d{4})",
        "Issue Date": r"issued\s*(?P<issue>\d{2}/\d{2}/\d{4})"
    }
    data = []
    for label, pattern in regex_patterns.items():
        match = re.search(pattern, text)
        if match:
            for group_name in match.groupdict():
                data.append({
                    "Label": label,
                    "Id Info": match.group(group_name),
                    "Regex Pattern": pattern
                })

    return data