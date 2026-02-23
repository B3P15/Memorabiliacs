import streamlit as st
from google.cloud import firestore
import global_functions as gfuncs
import BackendMethods.auth_functions as authFuncs
import BackendMethods.backendfuncs as backEnd

# user sign-in check
if 'user_info' not in st.session_state:
    st.switch_page("pages/login.py")
## -------------------------------------------------------------------------------------------------
## Logged in ---------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
else:
    gfuncs.page_initialization()
# This is straight from kieran's ui in apitesting, placeholder
    st.title("Search for Collectables!", text_alignment="center")
    # DEGUB:{st.session_state.user_info}
    st.space("large")
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
                    upc_result = backEnd.test_upc_api(upc_query)
                    # for idx, result in enumerate(upc_result):
                    with cols[0]:
                       if upc_result["image"]:
                           st.image(upc_result["image"], width=200)
                       st.write(f"**{upc_result.get('title', 'No title')}**")
                       if upc_result["description"]:
                           st.write(f"Description: {upc_result['description']}")
                    st.write(f"Item ean: {upc_result['ean']}")

                except Exception as e:
                    st.error(f"UPC search failed: {e}")
    elif search_type == "Pokemon Cards":
        with st.form(key="algolia_search_form", clear_on_submit=False):
            pokemon_query = st.text_input("Search for a Pokemon card")
            pokemon_search_submitted = st.form_submit_button("Search Pokemon")

        if pokemon_search_submitted:
            with st.spinner("Searching Pokemon (Algolia)..."):
                try:
                    algolia_conf = st.secrets.get("algolia", {})
                    app_id = algolia_conf.get("app_id")
                    search_key = algolia_conf.get("search_key")

                    if not (app_id and search_key):
                        raise ValueError("Algolia credentials (app_id, search_key, index_name) missing in Streamlit secrets")

                    hits = backEnd.search_algolia(pokemon_query, index_name="PokemonSearchResults", max_results=10)
                except Exception as e:
                    st.error(f"Algolia search failed: {e}")
                    hits = []

            st.session_state["pokemon_results"] = hits

            pokemon_results = st.session_state.get("pokemon_results", [])
            if pokemon_results:
                st.markdown("### Top Pokemon results")
                cols = st.columns(2)
                for idx, item in enumerate(pokemon_results):
                    with cols[idx % 2]:
                        if item.get("image"):
                            st.image(item["image"], width=200)
                        name = item.get('name', item.get('title', 'No name'))
                        st.write(f"**{name}**")
                        if item.get('set'):
                            st.write(item['set'])
                        if item.get('HP'):
                            st.write(f"HP: {item['HP']}")
                        if item.get('flavorText'):
                            st.write(f"*{item['flavorText']}*")
                        st.write(f"ID: {item['id']}")
    else:
        st.info("Search functionality for this category is coming soon!")