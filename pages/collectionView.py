import streamlit as st
from google.cloud import firestore
import global_functions as gfuncs
import BackendMethods.auth_functions as authFuncs
import BackendMethods.backendfuncs as backEnd

# Connects to db
try:
    db = firestore.Client.from_service_account_info(st.secrets["firebase"])
except Exception as e:
    st.error(f"Failed to initialize Firestore: {e}")
    st.stop()    

# user sign-in check
if 'user_info' not in st.session_state:
    st.switch_page("pages/login.py")
## -------------------------------------------------------------------------------------------------
## Logged in ---------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
else:
    gfuncs.page_initialization()

    user_id = st.session_state.user_info["localId"]
    collectionData = backEnd.generate_collection(backEnd.CURR_COLL, db)
    st.space("small")
    st.subheader(backEnd.CURR_COLL.split("_")[0], text_alignment="center")
    st.space("small")

    # view selection radio buttons
    view_mode = st.radio("Display mode", ["grid", "column"], horizontal=True)

    
        # Edit dialog to change the name of the collection
        # @st.dialog("Edit") 
        # def editCollection(coll):
        #     with st.container(horizontal=True, horizontal_alignment="center"):
        #         st.subheader(f"Rename {coll.id.split("_")[0]}?", text_alignment="center")
        #         coll_rename = st.text_input(" ")
        #         if st.button ("Rename", key=f"rename_{coll.id.split("_")[0]}", width="content"):
        #             if backEnd.renameCollection(coll, coll_rename, db):
        #                 st.error("Collection name already exist")
        #             else: 
        #                 st.rerun()

        # # Add collection dialog for adding a new collection to the db
        # @st.dialog("Add")
        # def addCollection():
        #     name = st.text_input("Name the Collection")
        #     collType = st.text_input("Give Collection Type") # will be dropdown
        #     if st.button("Add", key="makeColl") and name is not None and collType is not None:
        #         if backEnd.create_collection(name, collType, db):
        #             st.error("Collection name already exist")
        #         else:
        #             st.rerun()

        # # Remove collection dialog to remove a collection from the db
        # @st.dialog("Remove") 
        # def removeCollection(coll):
        #     with st.container(horizontal=True, horizontal_alignment="center"):
        #         st.subheader(f"Are you sure you want to remove \"{coll.split("_")[0]}\"?", text_alignment="center")
        #         if st.button("Yes", key=f"confirmRemove", width="content"):
        #             ref = db.collection("Users").document(user_id).collection("Collections").document(coll)
        #             ref.delete()
        #             st.rerun()
                
        #         if st.button("No", key=f"cancelRemove", width="content"):
        #             st.rerun()

        # iterate through collections and collect item info
    items = []
    for id, ref in collectionData.items():
        if id == "Info":
            continue
        doc = ref.get()
        if doc.exists:
            info = doc.to_dict()
            items.append(info)

    # display either grid or column view
    if view_mode == "grid":
        with st.container(horizontal=True, horizontal_alignment="center", width="stretch"):
            cols = st.columns(3, width="stretch")  # grid view
            for idx, info in enumerate(items):
                col = cols[idx % 3]
                with col.container(horizontal_alignment="center"):
                    st.subheader(f"{info.get('name','')}", text_alignment="center")
                    st.image(info.get('image',''), width="content")
                    for key, val in info.items():
                        if key not in ("name", "image"):
                            st.write(f"{key}: {val}")
                    st.space("medium")
    else:
        with st.container(horizontal=False, horizontal_alignment="center", width="stretch"):
            cols = st.columns([0.2,0.8,0.2], width="stretch")  # column view (default)
            for info in items:
                with cols[1].container(width="stretch", horizontal_alignment="center"):
                    st.subheader(f"{info.get('name','')}", text_alignment="center")
                    st.image(info.get('image',''), width=300)
                    for key, val in info.items():
                        if key not in ("name", "image"):
                            st.markdown(f"<p style='text-align: center;'>{key}: {val}</p>", unsafe_allow_html=True)
                    st.space("medium")
                st.space("small")



    # Container in bottom right for add button
    
    with st.container(horizontal=True, horizontal_alignment="right"):
        # Text box for input
        item_id = st.text_input("Enter Item ID")
        new_string = ""
        for i in range(len(item_id)):
            if item_id[i] == "-":
                 new_string+="_"
            else:
                new_string+=item_id[i]
        # Add to collection button. Must input Id for now
        if st.button("Add To Collection"):
            backEnd.add_reference(db, user_id, new_string, item_id)
        if st.button("Remove From Collection"):
            backEnd.delete_reference(db, user_id, new_string)