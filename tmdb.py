import tmdbsimple as tmdb
import streamlit as st

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