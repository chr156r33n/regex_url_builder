import re
import streamlit as st
from collections import defaultdict

def optimize_regex(patterns):
    """
    Optimize regex patterns by grouping common prefixes and suffixes.
    
    Args:
        patterns (list of str): List of individual regex patterns.

    Returns:
        str: Optimized regex string.
    """
    prefix_dict = defaultdict(list)
    for pattern in patterns:
        parts = pattern.split("/")
        prefix = parts[0] if parts else ""
        prefix_dict[prefix].append(pattern)
    
    optimized_patterns = []
    for prefix, paths in prefix_dict.items():
        if len(paths) > 1:
            suffixes = [p[len(prefix):] for p in paths]
            optimized_patterns.append(f"{prefix}({ '|'.join(suffixes) })")
        else:
            optimized_patterns.append(paths[0])
    
    return "|".join(optimized_patterns)

def build_regex(urls, domain, wild_start=False, wild_end=False, case_sensitive=True, negative_match=False):
    """
    Builds regex patterns based on user preferences and optimizes them.

    Args:
        urls (list of str): List of URLs.
        domain (str): Domain to strip from the URLs.
        wild_start (bool): Add wildcards at the start of the regex.
        wild_end (bool): Add wildcards at the end of the regex.
        case_sensitive (bool): Make the regex case-sensitive or not.
        negative_match (bool): Create a negative match regex.

    Returns:
        str: Generated and optimized regex pattern.
    """
    flags = 0 if case_sensitive else re.IGNORECASE
    
    stripped_paths = []
    for url in urls:
        stripped_url = re.sub(rf"https?://{re.escape(domain)}/?", "", url.strip(), flags=flags)
        stripped_paths.append(stripped_url)
    
    regex_parts = []
    for path in stripped_paths:
        if not wild_start:
            path = "^" + path.lstrip("/")  # Ensure no leading slash in regex
        if not wild_end:
            path += "$"
        regex_parts.append(path)
    
    optimized_regex = optimize_regex(regex_parts)
    optimized_regex = optimized_regex.replace("/", r"\/")
    
    if negative_match:
        optimized_regex = f"^(?!{optimized_regex}).*$"
    
    return optimized_regex

# Streamlit App
st.title("Regex Generator for URL Matching")
st.markdown("By Chris Green [www.chris-green.net](https://www.chris-green.net/)")

# URL Input
st.subheader("Enter URLs")
url_input = st.text_area(
    "Paste your URLs (one per line):",
    placeholder="https://example.com/path1\nhttp://example.com/path2\nhttps://example.com/path3",
    height=200
)
urls = url_input.splitlines() if url_input.strip() else []

if urls:
    st.success(f"Detected {len(urls)} URLs.")

    domain = st.text_input("Enter the domain to strip (e.g., example.com):")
    wild_start = st.checkbox("Allow wildcard matching at the start of the string", value=False)
    wild_end = st.checkbox("Allow wildcard matching at the end of the string", value=False)
    case_sensitive = st.checkbox("Case-sensitive matching", value=True)
    negative_match = st.checkbox("Generate a negative match regex", value=False)

    if domain:
        regex = build_regex(urls, domain, wild_start, wild_end, case_sensitive, negative_match)
        st.subheader("Generated Regex:")
        st.code(regex)

        st.subheader("Regex Tester")
        test_strings = st.text_area("Enter test strings (one per line):", height=150)
        if test_strings.strip():
            st.write("### Test Results:")
            test_results = []
            flags = 0 if case_sensitive else re.IGNORECASE
            for test_string in test_strings.splitlines():
                match = re.search(regex, test_string.strip(), flags=flags)
                test_results.append(f"✅ `{test_string.strip()}`" if match else f"❌ `{test_string.strip()}`")
            st.text("\n".join(test_results))

with st.expander("Instructions: How to Use This App"):
    st.markdown("""
    ### Steps to Use the Regex Generator:
    1. **Enter URLs**:
       - Paste URLs directly into the "Enter URLs" text field (one URL per line).
    2. **Configure Regex Options**:
       - **Enter Domain**: Provide the domain you want to strip (e.g., `example.com`).
       - **Wildcard Options**: Enable partial matching at the start or end.
       - **Case Sensitivity**: Enable/Disable case-sensitive matching.
       - **Negative Match**: Exclude URLs that match the patterns.
    3. **Generate and Test the Regex**.
    """)
