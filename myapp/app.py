import streamlit as st
import os

# Set the upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# User authentication and roles
users = {
    "admin": {"password": "adminpass", "role": "admin"},
    "user": {"password": "userpass", "role": "user"}
}

def login(username, password):
    if username in users and users[username]["password"] == password:
        return users[username]["role"]
    return None

# Streamlit app
st.set_page_config(page_title="Gallery App", layout="wide")
st.title("Gallery App")

# Login form
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

if not st.session_state.logged_in:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        role = login(username, password)
        if role:
            st.session_state.logged_in = True
            st.session_state.role = role
            st.success(f"Logged in successfully as {role}!")
        else:
            st.error("Invalid username or password.")
else:
    st.subheader("Gallery")
    
    # Display uploaded files
    if os.listdir(UPLOAD_FOLDER):
        st.markdown("<div class='gallery'>", unsafe_allow_html=True)
        for file in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, file)
            if file.endswith(('mp4', 'mov')):
                st.video(file_path)
            else:
                st.image(file_path)

            # Delete file button (only for admin)
            if st.session_state.role == "admin":
                if st.button(f"Delete {file}", key=file):
                    os.remove(file_path)
                    st.success(f"{file} deleted successfully!")
                    st.experimental_rerun()  # Refresh the app to update the gallery
        st.markdown("</div>", unsafe_allow_html=True)

    # Admin upload section
    if st.session_state.role == "admin":
        st.subheader("Upload Images or Videos")
        uploaded_files = st.file_uploader("Choose files", type=['jpg', 'jpeg', 'png', 'mp4', 'mov'], accept_multiple_files=True)

        if uploaded_files:
            for uploaded_file in uploaded_files:
                # Save uploaded files to the upload folder
                with open(os.path.join(UPLOAD_FOLDER, uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
            st.success("Files uploaded successfully!")

    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.success("Logged out successfully!")

# Add custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f5;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #0095f6;
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
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #007bb5;
    }
    h1, h2 {
        color: #333;
    }
    .stTextInput>div>input {
        border: 1px solid #0095f6;
        border-radius: 5px;
        padding: 10px;
    }
    .stTextInput>div>input:focus {
        border-color: #007bb5;
    }
    .gallery {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: center;
    }
    .gallery img, .gallery video {max-width: 100%;
        height: auto;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)