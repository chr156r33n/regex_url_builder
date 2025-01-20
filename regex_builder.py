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
    flags = 0 if case_sensitive else re.IGNORECASE

    stripped_paths = []
    for url in urls:
        stripped_url = re.sub(rf"https?://{re.escape(domain)}/?", "", url.strip(), flags=flags)
        # Escape slashes but leave dashes unescaped
        stripped_url = stripped_url.replace("/", r"\/")
        stripped_paths.append(stripped_url)

    regex_parts = []
    for path in stripped_paths:
        if not wild_start:
            path = "^" + path
        if not wild_end:
            path += "$"
        regex_parts.append(path)

    pattern = "|".join(regex_parts)
    if negative_match:
        pattern = f"^(?!{pattern}).*$"

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
    if domain:
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

        # Real-Time Regex Tester
        st.subheader("Regex Tester")
        test_strings = st.text_area("Enter test strings (one per line):", height=150)
        if test_strings.strip():
            st.write("### Test Results:")
            test_results = []
            flags = 0 if case_sensitive else re.IGNORECASE
            for test_string in test_strings.splitlines():
                match = re.search(regex, test_string.strip(), flags=flags)
                if match:
                    test_results.append(f"✅ `{test_string.strip()}`")
                else:
                    test_results.append(f"❌ `{test_string.strip()}`")
                    
            # Join results with newlines for better readability
            st.text("\n".join(test_results))

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
       - The app will display the generated regex below the input fields.
    5. **Test the Regex in Real-Time**:
       - Enter test strings in the "Regex Tester" section to verify matches in real-time.
    6. **Download the Regex**:
       - Use the "Download Regex" button to save the regex as a `.txt` file.
    7. **Use the Regex**:
       - Copy the generated regex or use the downloaded file for your project.
    """)
