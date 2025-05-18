import streamlit as st
import json
import os
import hashlib
import re

USERS_FILE = "users.json"

def init_users_file():
    """Initialize the users file if it doesn't exist"""
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump({}, f)

def hash_password(password):
    """Hash the password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    """Validate email format"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def register_user(full_name, email, password):
    """Register a new user"""
    init_users_file()
    if not validate_email(email):
        return False, "Invalid email format"
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    if email in users:
        return False, "Email already registered"
    users[email] = {
        "full_name": full_name,
        "password": hash_password(password)
    }
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)
    return True, "Registration successful"

def login_user(email, password):
    """Authenticate a user"""
    init_users_file()
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    if email not in users:
        return False, "Email not found"
    if users[email]["password"] != hash_password(password):
        return False, "Incorrect password"
    st.session_state.user_email = email
    st.session_state.user_name = users[email]["full_name"]
    return True, "Login successful"

def get_user_info(email):
    """Get user information"""
    init_users_file()
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    if email in users:
        return users[email]
    return None

def is_authenticated():
    """Check if user is authenticated"""
    return "user_email" in st.session_state

def logout():
    """Logout the current user"""
    for key in ["user_email", "user_name"]:
        if key in st.session_state:
            del st.session_state[key]

def login_register_ui():
    """Streamlit UI for login/register"""
    st.markdown("## 🔐 EduTutor AI Login / Register")
    tab = st.tabs(["Login", "Register"])
    with tab[0]:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            success, msg = login_user(email, password)
            if success:
                st.success(msg)
                st.experimental_rerun()
            else:
                st.error(msg)
    with tab[1]:
        st.subheader("Register")
        full_name = st.text_input("Full Name", key="reg_name")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_password")
        if st.button("Register"):
            success, msg = register_user(full_name, email, password)
            if success:
                st.success(msg)
            else:
                st.error(msg)

import auth
if not auth.is_authenticated():
    auth.login_register_ui()
    st.stop()