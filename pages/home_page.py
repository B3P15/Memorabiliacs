import streamlit as st
from google.cloud import firestore
import global_functions as gfuncs
import temp_backend as dbOLD
import BackendMethods.auth_functions as authFuncs


try:
    db = firestore.Client.from_service_account_info(st.secrets["firebase"])
except Exception as e:
    st.error(f"Failed to initialize Firestore: {e}")
    st.stop()

if 'user_info' not in st.session_state:
    st.switch_page("pages/login.py")
## -------------------------------------------------------------------------------------------------
## Logged in --------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
else:

    with st.container(horizontal=True, vertical_alignment="top"):
        with st.container(horizontal_alignment="left", vertical_alignment="top"):
            if st.button("Logout"):
                authFuncs.sign_out()
                st.switch_page("pages/login.py")
        with st.container(horizontal_alignment="right", vertical_alignment="top"):
            if st.button("Settings"):
                st.switch_page("pages/settings.py")


    conf_file = ".streamlit/config.toml"

    user_id = st.session_state.user_info["localId"]
    user_data_dict = db.collection("Users").document(user_id).get().to_dict()
    
    gfuncs.update_config_val(conf_file, "base", user_data_dict["base"])
    gfuncs.update_config_val(conf_file, "backgroundColor", user_data_dict["backgroundColor"])
    gfuncs.update_config_val(conf_file, "textColor", user_data_dict["textColor"])
    if gfuncs.login_color_flag == 0:
        gfuncs.login_color_flag = 1
        st.rerun()

    st.title(f"Your Collections\n Hello {st.session_state.user_info["email"]}", text_alignment="center")
    # DEGUB:{st.session_state.user_info}
    st.space("large")

    collection_page = "pages/template.py"

    user = st.session_state.user_info["localId"]
    collections = list(db.collection("Users").document(user).collections())

    with st.container(horizontal=True, horizontal_alignment="center"):

        @st.dialog("Edit") 
        def collection_edit_display(coll):
            # will return to, can't remove from self included dictionary
            with st.container(horizontal=True, horizontal_alignment="center"):
                st.subheader(f"Rename {coll}?", text_alignment="center")
                temp_coll_rename = st.text_input(" ")
                if st.button ("Rename", key=f"rename_{coll}", width="content"):
                    gfuncs.rename(coll, temp_coll_rename, dbOLD.collection_list)
                    st.rerun()

        # iterate through collections
        for coll in collections:
            # st.subheader(f"{list(coll.stream())}", text_alignment="center")
            for doc in list(coll.stream()):
                # st.subheader(f"{doc.id}")
                with st.container(width="content", horizontal_alignment="center"):
                    st.subheader(f"{doc.id}", text_alignment="center")
                    if st.button("View Collection", key=f"{doc.id}_link"):
                        dbOLD.current_coll = doc.id
                        st.switch_page(collection_page)
                    if st.button("Edit", key=f"edit_{doc.id}"):
                        collection_edit_display(doc.id)
                    if st.button("Remove", key=f"remove_{doc.id}", width="content"):
                        dbOLD.collection_list.remove(doc.id)
                        st.rerun()
                    st.space("medium")
                st.space("small")
        
        # add collection
        @st.dialog("Add")
        def addCollection():
            name = st.text_input("Name the Collection")
            coll_type = st.text_input("Give Collection Type") # will be dropdown
            if st.button("Add", key="makePage") and name is not None and coll_type is not None:
                dbOLD.collection_list.append(name.title())
                coll_name = gfuncs.snake_name(name.strip())
                dbOLD.current_coll = coll_name
                st.rerun()
            

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
