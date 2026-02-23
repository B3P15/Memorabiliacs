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
    
    # variables
    conf_file = ".streamlit/config.toml"
    collection_page = "pages/collectionView.py"
    user_id = st.session_state.user_info["localId"]
    user_data_dict = db.collection("Users").document(user_id).get().to_dict()
    collections = list(db.collection("Users").document(user_id).collections())
    
    # Updates user configs
    gfuncs.update_config_val(conf_file, "base", user_data_dict["base"])
    gfuncs.update_config_val(conf_file, "backgroundColor", user_data_dict["backgroundColor"])
    gfuncs.update_config_val(conf_file, "textColor", user_data_dict["textColor"])
    if gfuncs.login_color_flag == 0:
        gfuncs.login_color_flag = 1
        st.rerun()

    ## -------------------------------------------------------------------------------------------------
    ## Main Page Setup ---------------------------------------------------------------------------------
    ## -------------------------------------------------------------------------------------------------
    st.title(f"Your Collections\n Hello {st.session_state.user_info['email']}", text_alignment="center")
    # DEGUB:{st.session_state.user_info}
    st.space("large")

    # Center section for collections
    with st.container(horizontal=True, horizontal_alignment="center"):

        # Edit dialog to change the name of the collection
        @st.dialog("Edit") 
        def editCollection(coll):
            with st.container(horizontal=True, horizontal_alignment="center"):
                st.subheader(f"Rename {coll.id.split('_')[0]}?", text_alignment="center")
                coll_rename = st.text_input(" ")
                if st.button ("Rename", key=f"rename_{coll.id.split('_')[0]}", width="content"):
                    if backEnd.renameCollection(coll, coll_rename, db):
                        st.error("Collection name already exist")
                    else: 
                        st.rerun()

        # Add collection dialog for adding a new collection to the db
        @st.dialog("Add")
        def addCollection():
            name = st.text_input("Name the Collection")
            collType = st.text_input("Give Collection Type") # will be dropdown
            if st.button("Add", key="makeColl") and name is not None and collType is not None:
                if backEnd.create_collection(name, collType, db):
                    st.error("Collection name already exist")
                else:
                    st.rerun()

        # Remove collection dialog to remove a collection from the db
        @st.dialog("Remove") 
        def removeCollection(coll):
            with st.container(horizontal=True, horizontal_alignment="center"):
                st.subheader(f"Are you sure you want to remove \"{coll.split('_')[0]}\"?", text_alignment="center")
                if st.button("Yes", key=f"confirmRemove", width="content"):
                    ref = db.collection("Users").document(user_id).collection("Collections").document(coll)
                    ref.delete()
                    st.rerun()
                
                if st.button("No", key=f"cancelRemove", width="content"):
                    st.rerun()

        # iterate through collections
        for coll in collections:
            for doc in list(coll.stream()):
                collInfo = doc.id.split('_')
                if not collInfo[0] == "DefaultCollection":
                    with st.container(width="content", horizontal_alignment="center"):
                        st.subheader(f"{collInfo[0]}", text_alignment="center")

                        if st.button("View Collection", key=f"{collInfo[0]}_link"):
                            backEnd.setCollection(doc.id)
                            st.switch_page(collection_page)

                        if st.button("Edit", key=f"edit_{collInfo[0]}"):
                            editCollection(doc)

                        if st.button("Remove", key=f"remove_{collInfo[0]}", width="content"):
                            removeCollection(doc.id)

                        st.space("medium")
                    st.space("small")

    # Container in bottom right for add button
    with st.container(horizontal=True, horizontal_alignment="right"):
        # add collection button
        if st.button("Add Collection"):
            addCollection()
    
# This is straight from kieran's ui in apitesting, placeholder
    st.header("Search Media")
    search_type = st.selectbox(
        "What would you like to search for?",
        options=("Vinyl & CDs", "Movies", "Pokemon Cards", "UPC"),
    )

    #if search_type == "Vinyl & CDs":
    #    with st.form(key="ia_search_form", clear_on_submit=False):
    #        creators = st.text_input("Creator(s) (comma-separated)")
    #        title = st.text_input("Title or track")
    #        ia_search_submitted = st.form_submit_button("Search Archive")
#
    #    if ia_search_submitted:
    #        with st.spinner("Searching Internet Archive..."):
    #            try:
    #                results = search_internetarchive(creators, title, max_results=10)
    #            except Exception as e:
    #                st.error(f"Search failed: {e}")
    #                results = []
    #        st.session_state["ia_results"] = results
#
    #    ia_results = st.session_state.get("ia_results", [])
    #    if ia_results:
    #        st.markdown("### Top 10 results")
    #        cols = st.columns(2)
    #        for idx, item in enumerate(ia_results):
    #            with cols[idx % 2]:
    #                if item.get("thumbnail"):
    #                    st.image(item["thumbnail"], width=200)
    #                st.write(f"**{item.get('title', 'No title')}**")
    #                if item.get("creator"):
    #                    st.write(item.get("creator"))
    #                st.write(f"ID: {item.get('identifier')}")
    #                if item.get("format"):
    #                    st.write(f"Format: {item.get('format')}")
#
    #                checkbox_key = f"music_add_{item.get('identifier')}"
    #                def _add_music(item=item, checkbox_key=checkbox_key):
    #                    try:
    #                        user_id = st.session_state.user_info["localId"]
    #                        item_id = item["identifier"]
#
    #                        # Ensure Music collection exists by creating a metadata doc if needed
    #                        music_collection_ref = db.collection("Music")
    #                        if not music_collection_ref.document(item_id).get().exists:
    #                            # Create the collection by adding the first item
    #                            pass
    #                        
    #                        music_ref = db.collection("Music").document(item_id)
    #                        music_ref.set(item)
#
    #                        user_collections = (
    #                            db.collection("Users")
    #                            .document(user_id)
    #                            .collection("Collections")
    #                            .document("Music")
    #                        )
    #                        user_collections.set({"items": []}, merge=True)
    #                        user_collections.update({
    #                            "items": firestore.ArrayUnion([music_ref])
    #                        })
#
    #                        st.success(f"Added '{item.get('title')}' to Music")
    #                    except Exception as e:
    #                        st.error(f"Failed to add to collection: {e}")
    #                    finally:
    #                        st.session_state[checkbox_key] = False
#
    #                st.checkbox("Add to Music", key=checkbox_key, on_change=_add_music)
#
    #elif search_type == "Movies":
    #    with st.form(key="tmdb_search_form", clear_on_submit=False):
    #        movie_query = st.text_input("Search for a movie")
    #        tmdb_search_submitted = st.form_submit_button("Search Movies")
#
    #    if tmdb_search_submitted:
    #        with st.spinner("Searching TMDB..."):
    #            try:
    #                results = search_movies(movie_query, max_results=10)
    #            except Exception as e:
    #                st.error(f"Search failed: {e}")
    #                results = []
    #        st.session_state["tmdb_results"] = results
    if search_type == "UPC":
        upc_query = st.text_input("Enter UPC code")
        if st.button("Search UPC"):
            with st.spinner("Searching UPC..."):
                try:
                    st.markdown("UPC search results:")
                    cols = st.columns(2)
                    #upc_result = test_upc_api(upc_query)
                    ## for idx, result in enumerate(upc_result):
                    #with cols[0]:
                    #    if upc_result["image"]:
                    #        st.image(upc_result["image"], width=200)
                    #    st.write(f"**{upc_result.get('title', 'No title')}**")
                    #    if upc_result["description"]:
                    #        st.write(f"Description: {upc_result['description']}")
                    #st.write(f"Item ean: {upc_result['ean']}")

                except Exception as e:
                    st.error(f"UPC search failed: {e}")