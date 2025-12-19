import global_functions as gfuncs

# stores dictionaries for prove of concept

collection_list = ['Pokemon Cards', 'Mugs', 'Movies', 'Video Games', 'Books', 'Vinyls']

current_coll = collection_list[0]

# vinyls
vinyl_names = [
    "Heavy Metal",
    "Script for a Jester's Tear",
    "Magnolia Electric Co. (Deluxe Edition)",
    "The Natural Bridge", "Manning Fireworks",
    "The Lonesome Crowded West",
    "Fragile",
    "The Power and the Glory",
    "The Royal Scam",
    "The Last Record Album",
    "Crime of the Century",
    "Dirt",
    "Rumours",
    ]
vinyl_pictures = [
    "https://f4.bcbits.com/img/a2926452844_10.jpg",
    "https://upload.wikimedia.org/wikipedia/en/a/a7/Marillion_-_Script_for_a_Jester%27s_Tear.jpg",
    "https://f4.bcbits.com/img/a3722717630_10.jpg",
    "https://f4.bcbits.com/img/a1990333595_10.jpg",
    "https://i.scdn.co/image/ab67616d0000b273b18fae872e1700b83e72a15b",
    "https://f4.bcbits.com/img/a0948178435_16.jpg",
    "https://i.scdn.co/image/ab67616d0000b27356325ff85cba9491cf55c215",
    "https://m.media-amazon.com/images/I/516+afvqIQL._UF1000,1000_QL80_.jpg",
    "https://i.scdn.co/image/ab67616d0000b2736ac9fc028a8ba4c13b34a784",
    "https://m.media-amazon.com/images/I/71lhuJVJ--L._UF1000,1000_QL80_.jpg",
    "https://i.discogs.com/xWx0iVcEvYxYGQssERYteNt4U9z70ewwsR6PAgSwLMM/rs:fit/g:sm/q:90/h:600/w:600/czM6Ly9kaXNjb2dz/LWRhdGFiYXNlLWlt/YWdlcy9SLTE0MTE5/NjAtMTMyMTM4NzU3/NS5qcGVn.jpeg",
    "https://i.etsystatic.com/47228966/r/il/300956/6256969742/il_fullxfull.6256969742_3i5u.jpg",
    "https://i.scdn.co/image/ab67616d0000b27357df7ce0eac715cf70e519a7"
]

global vinyl_list
vinyl_list = dict(zip(vinyl_names, vinyl_pictures))

# mugs
mug_names = [
    "Cat Mug",
    "Winter Mug",
    "Beach Mug",
    "Seabees"
    ]

mug_pictures = []
for mug in mug_names:
    mug_pictures.append(mug.lower().replace(" ", "_"))

global mug_list
mug_list = gfuncs.create_page_dict(mug_names)