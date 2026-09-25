import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
)

st.title("⚖️ LegalEase")
st.subheader("AI-Assisted Legal Document Drafting")

st.write(
    "Create a legal document draft using your document details and terms."
)

st.divider()

document_type = st.text_input(
    "Document Type",
    placeholder="Example: Non-Disclosure Agreement",
)

parties = st.text_area(
    "Parties Involved",
    placeholder="Example: Party A: ABC Company\nParty B: XYZ Company",
)

terms = st.text_area(
    "Terms and Conditions",
    placeholder="Enter the terms and conditions...",
)

effective_date = st.text_input(
    "Effective Date",
    placeholder="Example: 24 September 2026",
)

if st.button("Generate Document", type="primary"):

    if not document_type or not parties or not terms or not effective_date:
        st.warning("Please fill in all the fields.")
    else:
        with st.spinner("Generating document..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json={
                        "document_type": document_type,
                        "parties": parties,
                        "terms": terms,
                        "effective_date": effective_date,
                    },
                    timeout=120,
                )

                if response.status_code == 200:
                    data = response.json()

                    st.success("Document generated successfully!")

                    st.subheader("Generated Document")

                    content = st.text_area(
                        "Edit your document",
                        value=data["content"],
                        height=500,
                    )

                    st.download_button(
                        "Download TXT",
                        data=content,
                        file_name="legalease_document.txt",
                        mime="text/plain",
                    )

                else:
                    st.error(
                        f"Backend error: {response.status_code}"
                    )
                    st.code(response.text)

            except requests.exceptions.ConnectionError:
                st.error(
                    "Cannot connect to the LegalEase backend. "
                    "Make sure FastAPI is running on port 8000."
                )

            except Exception as e:
                st.error(f"Error: {e}")

st.divider()

st.caption(
    "Disclaimer: This is an AI-generated draft and should be reviewed "
    "by a qualified legal professional before signing or relying on it."
)