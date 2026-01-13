###############################################################
#   Author(s): Cooper Wooten, Kieran Gilpin
#   Desc: Basic version of login page for memorabiliacs using streamlit
###############################################################
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from sqlalchemy import text, Column, Integer, String, VARCHAR
from sqlalchemy.orm import declarative_base
from streamlit_authenticator.utilities import (CredentialsError,
                                               ForgotError,
                                               Hasher,
                                               LoginError,
                                               RegisterError,
                                               ResetError,
                                               UpdateError)

conn = st.connection('mysql', type='sql')
conn.session.execute(text("use user_database;"))
conn.session.commit()
test = conn.query('select U.UserID from Users as U;')
st.write(test)

st.success("Raw insert executed")


with open('.streamlit/config.yaml') as file:
     config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])


Base = declarative_base()

class User(Base):
     __tablename__ = "users"

     id = Column(Integer, primary_key=True)
     UserID= Column(VARCHAR(100))
     Username= Column(VARCHAR(100))
     PersonalDB= Column(VARCHAR(100))

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


#widget that registers a new user

try:
     (email,
     username,
     name) = authenticator.register_user(roles=["viewer"], clear_on_submit=True, merge_username_email=True, password_hint=False)
     if email:
          #upon proper user registration, store user information in sql database for use as foreign key
          #include placeholder variables to prevent against SQL injection
          with conn.engine.begin() as connection:
               connection.execute(
               text("""
               INSERT INTO users (UserID, Username, PersonalDB)
               VALUES (:UserID, :Username, :PersonalDB)
           """),
          {
            "UserID": email,
            "Username": username,
            "PersonalDB": f"{username}DB"
          }
    )

          st.success('User registered successfully')
except RegisterError as e:
     st.error(e)

#update the config file!
with open('.streamlit/config.yaml', 'w') as file:
     yaml.dump(config, file, default_flow_style=False, allow_unicode=True)

#callback=st.switch_page("pages/home_page.py")
# with st.container(horizontal=True, horizontal_alignment="center"):
#     username = st.text_input(label="Username")
#     password = st.text_input(label="Password", type="password")

# if st.button("Login"):
#     if username == "" or password == "":
#             st.error("Enter both a Username and a Password to login.")
#     elif username != "" and password != "":
#         st.switch_page("pages/home_page.py")