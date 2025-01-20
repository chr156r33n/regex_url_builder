import re
import streamlit as st

def build_regex(urls, domain, wild_start=False, wild_end=False, case_sensitive=True, negative_match=False):
    """
    Builds regex patterns based on user preferences.

    Args:
        urls (list of str): List of URLs.
        domain (str): Domain to strip from the URLs.
        wild_start (bool): Add wildcards at the start of the regex.
        wild_end (bool): Add wildcards at the end of the regex.
        case_sensitive (bool): Make the regex case-sensitive or not.
        negative_match (bool): Create a negative match regex.

    Returns:
        str: Generated regex pattern.
    """
    # Define the regex flags
    flags = 0 if case_sensitive else re.IGNORECASE

    # Strip protocol and domain (handle http and https)
    stripped_paths = []
    for url in urls:
        stripped_url = re.sub(rf"https?://{re.escape(domain)}/?", "", url.strip(), flags=flags)
        stripped_paths.append(re.escape(stripped_url))  # Escape special regex characters

    # Build the regex pattern
    regex_parts = []
    for path in stripped_paths:
        # Add anchors or wildcards as specified
        if not wild_start:
            path = "^" + path  # Anchor to start of string
        if not wild_end:
            path += "$"  # Anchor to end of string
        
        regex_parts.append(path)

    # Combine parts into a single pattern
    pattern = "|".join(regex_parts)  # Match any of the URLs
    
    if negative_match:
        pattern = f"^(?!{pattern}).*$"  # Negative lookahead to exclude matches

    return pattern


# Streamlit App
st.title("Regex Generator for URL Matching")

# File Upload
uploaded_file = st.file_uploader("Upload a .txt file with URLs", type="txt")
if uploaded_file:
    urls = uploaded_file.read().decode("utf-8").splitlines()
    st.success("File uploaded successfully!")

    # User Inputs
    domain = st.text_input("Enter the domain to strip (e.g., example.com):")
    wild_start = st.checkbox("Allow wildcard matching at the start of the string", value=False)
    wild_end = st.checkbox("Allow wildcard matching at the end of the string", value
