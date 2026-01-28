import json
import os

import streamlit as st
from google.cloud import firestore

from apitcg2 import get_cards2
from auth_functions import (
    create_account,
    delete_account,
    reset_password,
    sign_in,
    sign_out,
)
from internetarch import search_internetarchive
from tmdb import search_movies

# Initialize Firestore client
# The credentials are grabbed from Streamlit secrets
try:
    db = firestore.Client.from_service_account_info(st.secrets["firebase"])
except Exception as e:
    st.error(f"Failed to initialize Firestore: {e}")
    st.stop()


if 'user_info' not in st.session_state:
    col1, col2, col3 = st.columns([1, 2, 1])

    # Authentication form layout
    do_you_have_an_account = col2.selectbox(
        label='Do you have an account?',
        options=('Yes', 'No', 'I forgot my password')
    )
    auth_form = col2.form(key='Authentication form', clear_on_submit=False)
    email = auth_form.text_input(label='Email')
    password = (
        auth_form.text_input(label='Password', type='password')
        if do_you_have_an_account in {'Yes', 'No'}
        else auth_form.empty()
    )
    auth_notification = col2.empty()

    if (do_you_have_an_account == 'Yes' and
            auth_form.form_submit_button(
                label='Sign In', use_container_width=True, type='primary')):
        with auth_notification, st.spinner('Signing in'):
            sign_in(email, password, db)

    # Create Account
    elif (do_you_have_an_account == 'No' and
            auth_form.form_submit_button(
                label='Create Account', use_container_width=True, type='primary')):
        with auth_notification, st.spinner('Creating account'):
            create_account(email, password)

    # Password Reset
    elif (do_you_have_an_account == 'I forgot my password' and
            auth_form.form_submit_button(
                label='Send Password Reset Email',
                use_container_width=True, type='primary')):
        with auth_notification, st.spinner('Sending password reset link'):
            reset_password(email)

    # Authentication success and warning messages
    if 'auth_success' in st.session_state:
        auth_notification.success(st.session_state.auth_success)
        del st.session_state.auth_success
    elif 'auth_warning' in st.session_state:
        auth_notification.warning(st.session_state.auth_warning)
        del st.session_state.auth_warning

## -------------------------------------------------------------------------------------------------
## Logged in --------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
else:
    # Show user information
    st.header('User information:')
    st.write(st.session_state.user_info)

    # Sign out
    st.header('Sign out:')
    st.button(label='Sign Out', on_click=sign_out, type='primary')

    # Delete Account
    st.header('Delete account:')
    password = st.text_input(label='Confirm your password', type='password')
    st.button(
        label='Delete Account',
        on_click=delete_account,
        args=[password, db],
        type='primary'
    )

    # Internet Archive search UI (visible only when logged in)
    st.header("Search Media")
    search_type = st.selectbox(
        "What would you like to search for?",
        options=("Vinyl & CDs", "Movies")
    )

    if search_type == "Vinyl & CDs":
        with st.form(key='ia_search_form', clear_on_submit=False):
            creators = st.text_input('Creator(s) (comma-separated)')
            title = st.text_input('Title or track')
            ia_search_submitted = st.form_submit_button('Search Archive')

        if ia_search_submitted:
            with st.spinner('Searching Internet Archive...'):
                try:
                    ia_results = search_internetarchive(
                        creators, title, max_results=10
                    )
                except Exception as e:
                    st.error(f"Search failed: {e}")
                    ia_results = []

            if ia_results:
                st.markdown("### Top 10 results")
                cols = st.columns(2)
                for idx, item in enumerate(ia_results):
                    with cols[idx % 2]:
                        if item.get('thumbnail'):
                            st.image(item['thumbnail'], width=200)
                        st.write(f"**{item.get('title', 'No title')}**")
                        if item.get('creator'):
                            st.write(item.get('creator'))
                        st.write(f"ID: {item.get('identifier')}")
                        if item.get('format'):
                            st.write(f"Format: {item.get('format')}")

    elif search_type == "Movies":
        with st.form(key='tmdb_search_form', clear_on_submit=False):
            movie_query = st.text_input('Search for a movie')
            tmdb_search_submitted = st.form_submit_button('Search Movies')

        if tmdb_search_submitted:
            with st.spinner('Searching TMDB...'):
                try:
                    tmdb_results = search_movies(movie_query, max_results=10)
                except Exception as e:
                    st.error(f"Search failed: {e}")
                    tmdb_results = []

            if tmdb_results:
                st.markdown("### Top 10 results")
                cols = st.columns(2)
                for idx, movie in enumerate(tmdb_results):
                    with cols[idx % 2]:
                        if movie.get('poster_path'):
                            st.image(movie['poster_path'], width=200)
                        st.write(f"**{movie.get('title', 'No title')}**")
                        if movie.get('release_date'):
                            st.write(f"Release: {movie.get('release_date')}")
                        if movie.get('overview'):
                            st.write(movie.get('overview')[:200] + "...")
                        st.write(f"TMDB ID: {movie.get('tmdb_id')}")


# Page layout
    st.set_page_config(page_title="Pokemon Collection", layout="wide")

    st.title("🎴 My Pokemon Collection")

    # Get all available users
    try:
        all_users = [doc.id for doc in db.collection("Users").stream()]
    except Exception as e:
        st.error(f"Could not fetch users: {e}")
        all_users = []

    # User selection
    if all_users:
        user_id = st.selectbox("Select a User:", all_users)
    else:
        st.warning("No users found in database")
        user_id = None

    # Get all collections and documents for the selected user
    collection_doc = None
    subcollection_name = None

    if user_id:
        try:
            user_ref = db.collection("Users").document(user_id)
            subcollections = list(user_ref.collections())
            
            if subcollections:
                # Get all documents from all subcollections
                all_docs = {}
                for subcol in subcollections:
                    subcol_docs = list(subcol.stream())
                    for doc in subcol_docs:
                        all_docs[f"{subcol.id}/{doc.id}"] = (subcol.id, doc.id)
                
                if all_docs:
                    selected = st.selectbox("Select a Collection:", list(all_docs.keys()))
                    if selected:
                        subcollection_name, collection_doc = all_docs[selected]
                else:
                    st.info(f"No collections found for User {user_id}")
            else:
                st.info(f"No subcollections found for User {user_id}")
        except Exception as e:
            st.error(f"Could not fetch collections: {e}")

    cards_subcollection = "Cards"

    if user_id and collection_doc and subcollection_name:
        st.markdown(f"### {collection_doc}")
        st.write(f"Displaying all cards from User {user_id}'s {collection_doc}")

    # Add a debug section to show database structure
    with st.expander("🔍 Debug - Database Structure"):
        try:
            # Check what's in Users collection
            users_docs = list(db.collection("Users").stream())
            st.write(f"**Users in database:** {len(users_docs)}")
            for user_doc in users_docs:
                st.write(f"- User ID: {user_doc.id}")
                user_data = user_doc.to_dict()
                st.write(f"  Data: {user_data}")
                
                # Check subcollections for this user
                user_ref = db.collection("Users").document(user_doc.id)
                subcollections = list(user_ref.collections())
                st.write(f"  Subcollections: {[col.id for col in subcollections]}")
                
                for subcol in subcollections:
                    st.write(f"  - Subcollection: {subcol.id}")
                    # Show all documents in subcollection
                    sub_docs = list(subcol.stream())
                    st.write(f"    Documents in {subcol.id}: {len(sub_docs)}")
                    for sub_doc in sub_docs:
                        st.write(f"    - Doc: {sub_doc.id}, Data: {sub_doc.to_dict()}")
                        
                        # Check for nested subcollections
                        sub_ref = subcol.document(sub_doc.id)
                        nested_subcols = list(sub_ref.collections())
                        if nested_subcols:
                            st.write(f"      Nested Subcollections: {[col.id for col in nested_subcols]}")
                            for nested_col in nested_subcols:
                                nested_docs = list(nested_col.stream())
                                st.write(f"        - {nested_col.id}: {len(nested_docs)} documents")
                                for nested_doc in nested_docs:
                                    st.write(f"          - {nested_doc.id}: {nested_doc.to_dict()}")
        except Exception as debug_error:
            st.error(f"Debug error: {debug_error}")
            import traceback
            st.error(traceback.format_exc())

    try:
        if not user_id or not collection_doc or not subcollection_name:
            st.info("Please select a user and collection to view cards.")
        else:
            # Reference to the collection document using the correct subcollection name
            collection_ref = db.collection("Users").document(user_id).collection(subcollection_name).document(collection_doc)
            
            # Get the collection document
            collection_doc_data = collection_ref.get().to_dict()
            
            if not collection_doc_data:
                st.error(f"❌ Collection document '{collection_doc}' not found")
            elif "Cards" not in collection_doc_data:
                st.info(f"📭 No Cards field found in {collection_doc}. Start adding some!")
            else:
                # Get the list of card references
                card_references = collection_doc_data.get("Cards", [])
                
                if not card_references:
                    st.info(f"📭 No cards found in the {collection_doc}. Start adding some!")
                else:
                    # Display card count
                    st.success(f"✅ Found {len(card_references)} cards")
                    
                    # Create a grid layout for cards
                    cols = st.columns(3)
                    col_index = 0
                    
                    for card_ref in card_references:
                        try:
                            # Fetch the actual card document
                            card_doc = card_ref.get()
                            card_data = card_doc.to_dict()
                            st.write(f"**Debug - Processing Card:** {card_ref.path}, Data: {card_data}")
                            
                            display_data = card_data if card_data else None
                            
                            with cols[col_index % 3]:
                                # Display images at the top using st.image
                                if display_data:
                                    for key, value in display_data.items():
                                        if key.lower() in ['image', 'image_url', 'image_link']:
                                            if isinstance(value, str) and value.startswith(('http', 'gs://')):
                                                st.image(value, width='content')
                                
                                # Build card content as a formatted string
                                card_content = f"**Card Path:** {card_ref.path}\n\n"
                                
                                if display_data:
                                    # Display card details
                                    for key, value in display_data.items():
                                        if key.lower() in ['image', 'image_url', 'image_link']:
                                            # Skip images, already displayed above
                                            continue
                                        else:
                                            # Display other data as key-value pairs
                                            formatted_key = key.replace('_', ' ').title()
                                            card_content += f"**{formatted_key}:** {value}\n\n"
                                else:
                                    card_content += "*No additional data*\n\n"
                                
                            col_index += 1
                        except Exception as card_error:
                            st.error(f"Error loading card reference: {card_error}")

    except Exception as e:
        st.error(f"❌ Error fetching cards: {e}")
        import traceback
        st.error(traceback.format_exc())
        st.info("**Troubleshooting tips:**")
        st.write("""
        - Ensure your Firestore database path exists: `Users/{user_id}/Collections/{collection_name}`
        - Check that the collection document has a 'Cards' field with DocumentReferences
        - Verify your Firebase security rules allow read access
        """)

    # Footer
    st.divider()
    if st.button("🔄 Refresh Data"):
        st.rerun()


