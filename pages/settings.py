import streamlit as st
import global_functions as gfuncs

conf_file = ".streamlit/config.toml"

if st.button("Home"):
    st.switch_page("pages/home_page.py")

st.title("Settings", text_alignment="center")

st.set_page_config(layout="wide")

current_theme = gfuncs.read_config_val(conf_file, "base")
current_background_color = gfuncs.read_config_val(conf_file, "backgroundColor")
current_text_color = gfuncs.read_config_val(conf_file, "textColor")



with st.container(horizontal_alignment="left", vertical_alignment="top"):
    if current_theme == "dark":
        theme_choice = st.selectbox("Select base theme for app: ", ("Dark", "Light"))
    else:
        theme_choice = st.selectbox("Select base theme for app: ", ("Light", "Dark"))

    background_color_choice = st.color_picker("Select the background color: ", current_background_color)
    text_color_choice = st.color_picker("Select the text color: ", current_text_color)

with st.container(horizontal_alignment="right", vertical_alignment="bottom"):
    if st.button("Save Changes"):
        gfuncs.update_config_val(conf_file, "base", "dark" if theme_choice=="Dark" else "light")
        gfuncs.update_config_val(conf_file, "backgroundColor", background_color_choice)
        gfuncs.update_config_val(conf_file, "textColor", text_color_choice)
        st.rerun()

