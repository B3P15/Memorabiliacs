import streamlit as st
import global_functions as gfuncs
import temp_backend as db
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
collection_page_list = gfuncs.create_page_dict(db.collection_list)

if st.button("Settings"):
    st.switch_page("pages/settings.py")

st.title("Collections", text_alignment="center")
st.space("large")

authenticator.login(location="unrendered")

collection_page = "pages/template.py"

with st.container(horizontal=True, horizontal_alignment="center"):

    @st.dialog("Edit") 
    def collection_edit_display(coll):
        # will return to, can't remove from self included dictionary
        with st.container(horizontal=True, horizontal_alignment="center"):
            st.subheader(f"Rename {coll}?", text_alignment="center")
            temp_coll_rename = st.text_input(" ")
            if st.button ("Rename", key=f"rename_{coll}", width="content"):
                gfuncs.rename(coll, temp_coll_rename, db.collection_list)
                st.rerun()

    for coll in db.collection_list:

        with st.container(width="content", horizontal_alignment="center"):
            st.subheader(f"{coll}", text_alignment="center")
            if st.button("View Collection", key=f"{coll}_link"):
                db.current_coll = coll
                st.switch_page(collection_page)
            if st.button("Edit", key=f"edit_{coll}"):
                collection_edit_display(coll)
                pass
            if st.button("Remove", key=f"remove_{coll}", width="content"):
                    db.collection_list.remove(coll)
                    st.rerun()

            st.space("medium")
        
        st.space("small")
    
    # add collection
    @st.dialog("Add")
    def addCollection():
        name = st.text_input("Name the Collection")
        coll_type = st.text_input("Give Collection Type") # will be dropdown
        if st.button("Add", key="makePage") and name is not None and coll_type is not None:
            db.collection_list.append(name.title())
            coll_name = gfuncs.snake_name(name.strip())
            db.current_coll = coll_name
            st.rerun()
        

    with st.container(width="content", horizontal_alignment="center"):
        if st.button("Add Collection", key="add"):
            addCollection()
            pass

        # st.space("medium")
