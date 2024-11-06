import os

import pandas as pd
import streamlit as st

# Set the upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set the title of the app
st.title("Daily Gallery")

# File uploader
uploaded_files = st.file_uploader("Upload Images or Videos", type=['jpg', 'jpeg', 'png', 'mp4', 'mov'], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        # Save uploaded files to the upload folder
        with open(os.path.join(UPLOAD_FOLDER, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
    
    st.success("Files uploaded successfully!")

# Display uploaded files
if os.listdir(UPLOAD_FOLDER):
    st.subheader("Gallery")
    for file in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, file)
        if file.endswith(('mp4', 'mov')):
            st.video(file_path)
        else:
            st.image(file_path)

# Add custom CSS
st.markdown(
    """
    <style>
    body {
        background-color: #f4f4f4;
        font-family: Arial, sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
)
