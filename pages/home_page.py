import streamlit as st
import global_functions as gfuncs
import temp_backend as db
from google.cloud import firestore
from BackendMethods.backendfuncs import (
    get_cards2,
    search_internetarchive,
    generate_collection,
    search_movies,
    generate_login_template
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
    user_data_dict = newdb.collection("Users").document(user_id).get().to_dict()


    gfuncs.update_config_val(conf_file, "base", user_data_dict["base"])
    gfuncs.update_config_val(conf_file, "backgroundColor", user_data_dict["backgroundColor"])
    gfuncs.update_config_val(conf_file, "textColor", user_data_dict["textColor"])
    




    collection_page_list = gfuncs.create_page_dict(db.collection_list)

    if st.button("Settings"):
        st.switch_page("pages/settings.py")

    st.title("Collections", text_alignment="center")
    st.space("large")

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
