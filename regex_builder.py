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
    wild_end = st.checkbox("Allow wildcard matching at the end of the string", value=False)
    case_sensitive = st.checkbox("Case-sensitive matching", value=True)
    negative_match = st.checkbox("Generate a negative match regex", value=False)

    # Generate Regex
    if st.button("Generate Regex"):
        if not domain:
            st.error("Please enter a domain.")
        else:
            regex = build_regex(urls, domain, wild_start, wild_end, case_sensitive, negative_match)
            st.subheader("Generated Regex:")
            st.code(regex)

            # Option to download the regex
            st.download_button(
                label="Download Regex",
                data=regex,
                file_name="regex.txt",
                mime="text/plain"
            )

# Instructions Section
with st.expander("Instructions: How to Use This App"):
    st.markdown("""
    ### Steps to Use the Regex Generator:
    1. **Prepare Your File**:
       - Create a `.txt` file with one URL per line.
       - Example:
         ```
         https://example.com/path/to/resource
         http://example.com/another/path
         https://example.com/third/path
         ```
    2. **Upload the File**:
       - Use the "Upload a .txt file with URLs" option to upload your file.
    3. **Configure Regex Options**:
       - **Enter Domain**: Provide the domain you want to strip (e.g., `example.com`).
       - **Wildcard Options**:
         - Enable "Allow wildcard matching at the start of the string" to allow partial matches at the beginning.
         - Enable "Allow wildcard matching at the end of the string" to allow partial matches at the end.
       - **Case Sensitivity**:
         - Enable "Case-sensitive matching" for exact matches.
         - Disable it to ignore case differences.
       - **Negative Match**:
         - Enable "Generate a negative match regex" to exclude URLs that match the patterns.
    4. **Generate the Regex**:
       - Click "Generate Regex" to create the regex based on your settings.
    5. **Download the Regex**:
       - Use the "Download Regex" button to save the regex as a `.txt` file.
    6. **Use the Regex**:
       - Copy the generated regex or use the downloaded file for your project.
    """)

