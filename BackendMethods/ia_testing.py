import internetarchive


def search_internetarchive(creators: str = "", title: str = "", item_type: str = "audio", max_results: int = 10):
    """Search Internet Archive for items of a given type.

    creators: comma-separated list of creators to search (OR'd together)
    title: title or comma-separated titles to search (OR'd together)
    item_type: generic item type (e.g., 'audio', 'game', 'movie', 'text', 'image', 'software')
    max_results: maximum number of results to return (default 10)
    Returns a list of dicts with keys: identifier, title, creator, thumbnail, format, mediatype
    """
    # map common generic types to Internet Archive mediatype values
    type_map = {
        'game': 'software',
        'games': 'software',
        'software': 'software',
        'movie': 'movies',
        'movies': 'movies',
        'audio': 'audio',
        'song': 'audio',
        'songs': 'audio',
        'text': 'texts',
        'book': 'texts',
        'books': 'texts',
        'image': 'image',
        'images': 'image',
        'video': 'movies',
        '': '',  # no restriction
    }
    mediatype = type_map.get(item_type.lower(), item_type.lower())
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

    # limit to selected mediatype
    if mediatype:
        query_parts.append(f'mediatype:({mediatype})')

    query = " AND ".join(query_parts)

    search_results = internetarchive.search_items(
        query,
        fields=['identifier', 'title', 'creator', 'format', 'mediatype'],
    )

    results = []
    for result in search_results:
        if len(results) >= max_results:
            break
        identifier = result.get('identifier')
        name = result.get('title', '')
        creator = result.get('creator', '')
        fmt = result.get('format', '')
        mtype = result.get('mediatype', mediatype)
        thumb_url = f"https://archive.org/download/{identifier}/__ia_thumb.jpg" if identifier else None
        results.append({
            'identifier': identifier,
            'title': name,
            'creator': creator,
            'thumbnail': thumb_url,
            'format': fmt,
            'mediatype': mtype,
        })

    return results



# print('Audio results:')
#print(search_internetarchive("", "ninjago", item_type='audio', max_results=5))
#print('\nSoftware/game r   # print('Audio results:')esults:')
#print(search_internetarchive("", "coin", item_type='', max_results=5))

def printer(lod):
    for item in lod:
        print(item)

printer(search_internetarchive("", "ninjago", item_type='', max_results=5))