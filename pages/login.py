###############################################################
#   Author: Cooper Wooten
#   Desc: Basic version of login page for memorabiliacs using streamlit
###############################################################
import streamlit as st

st.title("Welcome Memorabiliac!", text_alignment="center")

with st.container(horizontal=True, horizontal_alignment="center"):
    username = st.text_input(label="Username")
    password = st.text_input(label="Password", type="password")

if st.button("Login"):
    if username == "" or password == "":
            st.error("Enter both a Username and a Password to login.")
    elif username != "" and password != "":
        st.switch_page("pages/home_page.py")