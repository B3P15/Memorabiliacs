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

st.title("Collections", text_alignment="center")
st.space("large")

authenticator.login(location="unrendered")

collection_page = "pages/template.py"

with st.container(horizontal=True, horizontal_alignment="center"):

    for coll in db.collection_list:
        
        @st.dialog("Delete") # center?
        def collection_edit_display():
            # will return to, can't remove from self included dictionary
            with st.container(horizontal=True, horizontal_alignment="center"):
                st.subheader(f"Are you sure you want to delete {coll}?", text_alignment="center")
                if st.button("Yes", key="delete_coll"):
                    db.collection_list.remove(coll)
                if st.button("No", key="close"):
                    # temp, returns to main page to remove popups
                    st.switch_page("pages/home_page.py")

        with st.container(width="content", horizontal_alignment="center"):
            st.subheader(f"{coll}", text_alignment="center")
            if st.button("View Collection", key=f"{coll}_link"):
                # st.switch_page(f"pages/{collection_page_list[coll]}.py")
                db.current_coll = coll
                st.switch_page(collection_page)
            if st.button("Edit", key=f"edit_{coll}"):
                collection_edit_display()

            st.space("medium")
        
        st.space("small")
    
    # add collection
    @st.dialog("Add")
    def addCollection():
        name = st.text_input("Name the Collection")
        coll_type = st.text_input("Give Collection Type") # will be dropdown
        if st.button("Add", key="makePage") and name is not None and coll_type is not None:
            coll_name = gfuncs.snake_name(name.strip())
            db.collection_list.append(coll_name)
            db.current_coll = coll_name
            st.switch_page(collection_page)
        

    with st.container(width="content", horizontal_alignment="center"):
        if st.button("Add Collection", key="add"):
            addCollection()
            pass

        # st.space("medium")
