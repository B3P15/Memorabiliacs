import internetarchive

def search_internetarchive():
    search_results = internetarchive.search_items(
        'creator:(Red Hot Chili Peppers) AND mediatype:(audio)',
        fields=['identifier', 'title']
    )
    url_list = []

    for result in search_results:
        identifier = result['identifier']
        name = result['title']
        # Construct thumbnail URL
        thumb_url = f"https://archive.org/download/{identifier}/__ia_thumb.jpg"
        url_list.append((thumb_url, name))
    return url_list
