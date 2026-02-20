import streamlit as st
import global_functions as gfuncs
from google.cloud import firestore
import BackendMethods.auth_functions as authFuncs
from BackendMethods.backendfuncs import (
    get_cards2,
    search_internetarchive,
    generate_collection,
    search_movies,
    generate_login_template,
    setCollection
)

try:
    newdb = firestore.Client.from_service_account_info(st.secrets["firebase"])
except Exception as e:
    st.error(f"Failed to initialize Firestore: {e}")
    st.stop()

if 'user_info' not in st.session_state:
    st.switch_page("pages/login.py")
## -------------------------------------------------------------------------------------------------
## Logged in --------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
else:

    conf_file = ".streamlit/config.toml"

    user_id = st.session_state.user_info["localId"]

    with st.container(horizontal=True, vertical_alignment="top"):
        with st.container(horizontal_alignment="left", vertical_alignment="top"):
            if st.button("Home"):
                st.switch_page("pages/home_page.py")
        with st.container(horizontal_alignment="right", vertical_alignment="top"):
            if st.button("Logout"):
                setCollection("")
                authFuncs.sign_out()
                st.switch_page("pages/login.py")


    st.title("Settings", text_alignment="center")

    st.set_page_config(layout="wide")

    current_theme = gfuncs.read_config_val(conf_file, "base")
    current_background_color = gfuncs.read_config_val(conf_file, "backgroundColor")
    current_text_color = gfuncs.read_config_val(conf_file, "textColor")
    current_font = gfuncs.read_config_val(conf_file, "font")



    with st.container(horizontal_alignment="left", vertical_alignment="top"):
        if current_theme == "dark":
            theme_choice = st.selectbox("Select base theme for app: ", ("Dark", "Light")).lower()
        else:
            theme_choice = st.selectbox("Select base theme for app: ", ("Light", "Dark")).lower()

        background_color_choice = st.color_picker("Select the background color: ", current_background_color)
        text_color_choice = st.color_picker("Select the text color: ", current_text_color)
        font_choice = st.selectbox("Select the font: ", ("serif", "sans-serif"), index=0 if current_font == "serif" else 1)

    with st.container(horizontal_alignment="right", vertical_alignment="bottom"):
        if st.button("Save Changes"):
            gfuncs.update_config_val(conf_file, "base", "dark" if theme_choice=="dark" else "light")
            gfuncs.update_config_val(conf_file, "backgroundColor", background_color_choice)
            gfuncs.update_config_val(conf_file, "textColor", text_color_choice)
            gfuncs.update_config_val(conf_file, "font", font_choice)
            newdb.collection("Users").document(user_id).set({"base" : theme_choice, 
                                                            "backgroundColor" : background_color_choice, 
                                                            "textColor" : text_color_choice,
                                                            "font" : font_choice},
                                                            merge=True)
            st.rerun()

