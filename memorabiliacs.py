import streamlit as st

# Initialize test user if session state is empty
if 'user_info' not in st.session_state:
    # Check if running in test mode (AppTest sets a marker)
    if hasattr(st, '_is_apptest') or 'STREAMLIT_TESTING' in st.secrets:
        st.session_state.user_info = {
            "localId": "test_user_123",
            "email": "test@example.com"
        }

st.switch_page("pages/login.py")