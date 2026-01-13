###############################################################
#   Author(s): Cooper Wooten, Kieran Gilpin
#   Desc: Basic version of login page for memorabiliacs using streamlit
###############################################################
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open('.streamlit/config.yaml') as file:
     config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

st.title("Welcome Memorabiliac!", text_alignment="center")


#This renders the login widget (popup)
try:
     authenticator.login()
except Exception as e:
     st.error(e)

if st.session_state["authentication_status"]:
     authenticator.logout()
     st.write(f'Welcome *{st.session_state["name"]}*')
     st.switch_page("pages/home_page.py")
elif st.session_state["authentication_status"] is False:
     st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
     st.warning('Please enter your username and password')

#callback=st.switch_page("pages/home_page.py")
# with st.container(horizontal=True, horizontal_alignment="center"):
#     username = st.text_input(label="Username")
#     password = st.text_input(label="Password", type="password")

# if st.button("Login"):
#     if username == "" or password == "":
#             st.error("Enter both a Username and a Password to login.")
#     elif username != "" and password != "":
#         st.switch_page("pages/home_page.py")