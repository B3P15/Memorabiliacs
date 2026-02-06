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
    for i in range(len(id)):
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

def search_movies(query:str, max_results:int=10):
    """Search TMDB for movies matching `query`.

        query(str): the query string to search for
        max_results (int): Default is 10. Maximum number of results to return
        Returns a list of dicts with keys: title, release_date, overview, poster_path, tmdb_id
    """

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

    creators(str): comma-separated list of creators to search (OR'd together)
    title(str): title or comma-separated titles to search (OR'd together)
    max_results(int): maximum number of results to return (default 10)
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
        items_refs = collection_doc.to_dict().get('items', [])
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
    auth_notification = col2.empty()


    if (do_you_have_an_account == 'Yes'):
        fields = {'Form name':'Login', 'Username':'Username', 'Password':'Password',
                        'Login':'Login'}

        login_form = st.form(key="Login", clear_on_submit=True)
        login_form.subheader('Login' if 'Form name' not in fields else fields['Form name'])
        email = login_form.text_input('Username' if 'Username' not in fields
                                                    else fields['Username'], autocomplete='off')
        password = login_form.text_input('Password' if 'Password' not in fields
                                                        else fields['Password'], type='password',
                                                        autocomplete='off')
        if login_form.form_submit_button('Login' if 'Login' not in fields
                                                    else fields['Login']):
            with auth_notification, st.spinner('Signing in'):
                sign_in(email, password, db)

    elif (do_you_have_an_account == 'No'):
        fields = {'Form name':'Create Account', 'Username':'Username', 'Password':'Password',
                        'Create Account':'Create Account'}
        create_account_form = st.form(key="Create Account", clear_on_submit=True)
        create_account_form.subheader('Create Account' if 'Form name' not in fields else fields['Form name'])
        email = create_account_form.text_input('Username' if 'Username' not in fields
                                                    else fields['Username'], autocomplete='off')
        password = create_account_form.text_input('Password' if 'Password' not in fields
                                                        else fields['Password'], type='password',
                                                        autocomplete='off')
        if create_account_form.form_submit_button('Create Account' if 'Create Account' not in fields
                                                    else fields['Create Account']):
            with auth_notification, st.spinner('Creating account'):
                create_account(email, password)
    elif (do_you_have_an_account == 'I forgot my password'):
        fields = {'Form name':'Reset Password', 'Username':'Username',
                        'Send Password Reset Email':'Send Password Reset Email'}
        reset_password_form = st.form(key="Reset Password", clear_on_submit=True)
        reset_password_form.subheader('Reset Password' if 'Form name' not in fields else fields['Form name'])
        email = reset_password_form.text_input('Username' if 'Username' not in fields
                                                    else fields['Username'], autocomplete='off')
        if reset_password_form.form_submit_button('Send Password Reset Email' if
                        'Send Password Reset Email' not in fields
                                                    else fields['Send Password Reset Email']):
            with auth_notification, st.spinner('Sending password reset link'):
                reset_password(email)
    if 'auth_success' in st.session_state:
        auth_notification.success(st.session_state.auth_success)
        del st.session_state.auth_success


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
            'minifig_id': item.get('set_num'),
            'image_url': item.get('set_img_url'),
        })

    return results

def search_sets_rebrickable(query, max_results: int = 10):
    """Search Rebrickable for sets matching `query`.

    Returns a list of dicts with keys: name, set_id, image_url, num_parts, year
    """
    rebrick.init(REBRICK_API_KEY)
    try:
        resp = rebrick.lego.get_sets(query)
        data = json.loads(resp.read())
    except Exception:
        return []

    items = []
    # this was from a unneccesarry check but it works so keeping it
    if isinstance(data, dict):
        items = data.get('results') 

    results = []
    for item in items[:max_results]:
        results.append({
            'name': item.get('name'),
            'set_id': item.get('set_num'),
            'image_url': item.get('set_img_url'),
            'num_parts': item.get('num_parts'),
            'year': item.get('year'),
        })

    return results