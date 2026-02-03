import internetarchive
import streamlit as st
import tmdbsimple as tmdb
import rebrick
import json
from fastapi import FastAPI, Query, Path, HTTPException
from requests_futures.sessions import FuturesSession
from concurrent.futures import as_completed
from BackendMethods.auth_functions import create_account, sign_in, reset_password

BASE_API_URL = "https://apitcg.com/api"
APITCG_API_KEY = st.secrets["APITCG_API_KEY"]  # change later

app = FastAPI()


# urls in format of 'https://apitcg.com/api/$GAME/cards?$ATTRIBUTE='

#Faster version of get_cards using asynchronous gets and future responses
@app.get("/{game}/cards")
def get_cards2(
    game: str = Path(..., description="Game type: one-piece, pokemon, yugioh, etc."),
    id: list[str] = Query(..., description="Card name(s) to search")
):
    url = f"{BASE_API_URL}/{game}/cards"

    headers = {
        "x-api-key": APITCG_API_KEY
    }


    futureList = []

    responseList = []
    session = FuturesSession()
    # first request is started in background
    for i in range(len(id)-1):
        params = {
        "id": id[i]}
        futureList.append(session.get(url, headers=headers, params=params))
    for future in as_completed(futureList):
        #create the dictionary with the id, name, type, hp, and image url
        try:
            card_hp = future.result().json()["data"][0]["hp"]
        except (KeyError, TypeError):
            card_hp = 0
        try:
            card_text = future.result().json()["data"][0]["flavorText"]
        except (KeyError, TypeError):
            card_text = ""
        card_name = future.result().json()["data"][0]["name"]
        card_id = future.result().json()["data"][0]["id"]
        image_url = future.result().json()["data"][0]["images"]["small"]
        responseList.append({
            "id": card_id,
            "flavorText": card_text,
            "hp": card_hp,
            "name": card_name,
            "image": image_url
        })

    return(responseList)


tmdb.API_KEY = st.secrets["TMDB_API_KEY"]

tmdb.REQUESTS_TIMEOUT = (2, 5)  # seconds, for connect and read specifically 

def search_movies(query, max_results=10):
    search = tmdb.Search()
    response = search.movie(query=query)
    results = []
    for movie in response['results'][:max_results]:
        results.append({
            'title': movie.get('title'),
            'release_date': movie.get('release_date'),
            'overview': movie.get('overview'),
            'poster_path': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else None,
            'tmdb_id': movie.get('id')
        })
    return results


def search_internetarchive(creators: str = "", title: str = "", max_results: int = 10):
    """Search Internet Archive for audio items filtered to Vinyl or CD formats.

    creators: comma-separated list of creators to search (OR'd together)
    title: title or comma-separated titles to search (OR'd together)
    max_results: maximum number of results to return (default 10)
    Returns a list of dicts with keys: identifier, title, creator, thumbnail, format
    """
    query_parts = []
    if creators:
        parts = []
        for c in creators.split(","):
            s = c.strip()
            if s:
                parts.append(f'"{s}"')
        creators_escaped = " OR ".join(parts)
        query_parts.append(f'creator:({creators_escaped})')
    if title:
        parts = []
        for t in title.split(","):
            s = t.strip()
            if s:
                parts.append(f'"{s}"')
        title_escaped = " OR ".join(parts)
        query_parts.append(f'title:({title_escaped})')

    # Always limit to audio mediatype
    query_parts.append('mediatype:(audio)')

    query = " AND ".join(query_parts)

    search_results = internetarchive.search_items(
        query,
        fields=['identifier', 'title', 'creator', 'format'],
    )

    results = []
    for result in search_results:
        identifier = result.get('identifier')
        name = result.get('title', '')
        creator = result.get('creator', '')
        fmt = result.get('format', '')
        thumb_url = f"https://archive.org/download/{identifier}/__ia_thumb.jpg" if identifier else None
        results.append({
            'identifier': identifier,
            'title': name,
            'creator': creator,
            'thumbnail': thumb_url,
            'format': fmt,
        })

    return results




#make a method to generate a specific collection (list of dictionaries) based on
#the input that will be the name of the collection. 
def generate_collection(collection_name: str, db):
    """Generate a collection of items from the database based on the collection name.

    collection_name: Name of the collection to retrieve
    db: Firestore database instance
    Returns a list of items (data dictionaries) referenced in the specified collection
    """
    user_id = st.session_state.user_info['localId']
    collection_ref = db.collection('Users').document(user_id).collection('Collections').document(collection_name)
    collection_doc = collection_ref.get()
    if collection_doc.exists:
        items_refs = collection_doc.to_dict().get('Cards', [])
        # Dereference each DocumentReference to get the actual data
        items_data = []
        for ref in items_refs:
            try:
                doc = ref.get()
                if doc.exists:
                    items_data.append(doc.to_dict())
            except Exception as e:
                st.error(f"Error dereferencing item: {e}")
        return items_data
    else:
        return []

#setup templates for login stuff
def generate_login_template(db):
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


REBRICK_API_KEY = st.secrets["REBRICK_API_KEY"]

def search_minifigs_rebrickable(query, max_results: int = 10):
    """Search Rebrickable for minifigs matching `query` (query can be part of any attribute present in the json, such as name or minifig_id).

    Returns a list of dicts with keys: name, minifig_id,  image_url

    """
    rebrick.init(REBRICK_API_KEY)
    try:
        resp = rebrick.lego.get_minifigs(query)
        data = json.loads(resp.read())
    except Exception:
        return []

    items = []
    if isinstance(data, dict):
        items = data.get('results')
  

    results = []
    for item in items[:max_results]:
        results.append({
            'name': item.get('name'),
            'minifig_id': item.get('set_num') or item.get('set'),
            'image_url': item.get('set_img_url'),
        })

    return results
