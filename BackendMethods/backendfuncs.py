import internetarchive
import streamlit as st
import tmdbsimple as tmdb
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
            'image': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else None,
            'id': movie.get('id')
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
            'id': identifier,
            'title': name,
            'creator': creator,
            'image': thumb_url,
            'format': fmt,
        })

    return results

# make a method to generate a specific collection (list of dictionaries) based on
# the input that will be the name of the collection. 
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
        items_refs = collection_doc.to_dict().get('items')
        # Dereference each DocumentReference to get the actual data
        # items_data = []
        # for ref in items_refs:
        #     # try:
        #     #     doc = ref.get()
        #     #     if doc.exists:
        #     #         items_data.append(doc.to_dict())
        #     # except Exception as e:
        #     #     st.error(f"Error dereferencing item: {e}")
        # return items_data
        return items_refs
    else:
        return []

# created new document in db
def create_collection(collection_name: str, collection_type: str, db):
    """Generate a collection of items from the database based on the collection name.

    collection_name: Name of the collection to retrieve
    db: Firestore database instance
    Returns a list of items (data dictionaries) referenced in the specified collection
    """
    user_id = st.session_state.user_info['localId']

    # generates db collection name
    fullName = collection_name.title() + f"_{collection_type}"

    # check if name already exists in the database
    if checkForCollName(collection_name, db):
        return True
    
    # created new collection
    db.collection('Users').document(user_id).collection('Collections').document(fullName).set({"items":[]})

# renames a collection
def renameCollection(collection_name:str, new_collection:str, db):
    """Renames a collection, by use of creating a new collection and moving the data
    
    collection_name: name of original collection
    new_collection: new name for collection
    db: database
    """
    user_id = st.session_state.user_info['localId']
    
    # gets reference and type of collection
    collection_ref_OLD = db.collection('Users').document(user_id).collection('Collections').document(collection_name.id)
    coll_Info = collection_ref_OLD.get().id.split("_")
    data = generate_collection(collection_name.id, db)
    # print(data)

    # checks if new name already exists in the database
    if checkForCollName(new_collection, db):
        return True

    # created new collection to move data to
    fullName = f"{new_collection.title()}_{coll_Info[1]}"
    db.collection('Users').document(user_id).collection('Collections').document(fullName).set({})
    items = {"items":[]}
    for coll in data:
        items['items'].append(coll)
    db.collection('Users').document(user_id).collection('Collections').document(fullName).set(items, merge=True)

    collection_ref_OLD.delete()

def checkForCollName(collection_name:str, db) -> bool:
    """Checks if the provided name is in the database
    
    collection_name: name checking for
    db: database
    """
    user_id = st.session_state.user_info['localId']

    collections = list(db.collection("Users").document(user_id).collections())

    for coll in collections:
        for doc in list(coll.stream()):
            collName = doc.id.split("_")
            if collName[0] == collection_name:
                return True
    return False
    

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
