import os
import sys
import tempfile
import traceback
import streamlit as st
from langchain.document_loaders import PyPDFLoader


try:
    # Setting page title and header
    st.set_page_config(page_title="PDF Reader",
                       )
    st.markdown("<h1 style='text-align: center;'>PDF Reader</h1>",
                unsafe_allow_html=True)

    def make_safe_filename(s):
        def safe_char(c):
            if c.isalnum():
                return c
            else:
                return "_"
        return "".join(safe_char(c) for c in s).rstrip("_")

    def get_correct_file_name(file_name):
        extension = os.path.splitext(file_name)[1]
        file_name = file_name.replace(extension, "")

        # Clean it in one fell swoop.
        new_file_name = make_safe_filename(file_name)
        new_file_name = new_file_name.replace("__", "_")
        new_file_name = new_file_name.replace("__", "_")
        new_file_name = new_file_name.replace("__", "_")
        new_file_name = new_file_name.replace("__", "_")

        first_char = new_file_name[0]
        if (first_char == '_'):
            new_file_name = new_file_name[1:]

        file_name = file_name + extension
        correct_file_name = new_file_name + extension

        return correct_file_name


    with st.form("pdf-reader-form"):
        uploaded_file = st.file_uploader(
            "Upload a PDF file:", type="pdf", key="uploaded_file")

        is_submitted = st.form_submit_button(
            label="Submit", )

        if is_submitted:
            temp_file_path = os.getcwd()

            if uploaded_file is not None:
                # Save the uploaded file to a temporary location
                temp_dir = tempfile.TemporaryDirectory()
                temp_file_path = os.path.join(temp_dir.name, uploaded_file.name)
                with open(temp_file_path, "wb") as temp_file:
                    temp_file.write(uploaded_file.read())

                # st.write("Full path of the uploaded file:", temp_file_path)

                # Create and load PDF Loader
                loader = PyPDFLoader(temp_file_path)
                # Split pages from pdf 
                docs = loader.load_and_split()

                for doc in docs:
                    st.info(doc.page_content)




except Exception as e:
    error_message = ''
    # st.text('Hello World')
    st.error('An error has occurred. Please try again.', icon="🚨")
    # Just print(e) is cleaner and more likely what you want,
    # but if you insist on printing message specifically whenever possible...
    if hasattr(e, 'message'):
        error_message = e.message
    else:
        error_message = e
    st.error('ERROR MESSAGE: {}'.format(error_message), icon="🚨")
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    st.error(f'Error Type: {exc_type}', icon="🚨")
    st.error(f'File Name: {fname}', icon="🚨")
    st.error(f'Line Number: {exc_tb.tb_lineno}', icon="🚨")
    st.error(traceback.format_exc())
