import streamlit as st

st.set_page_config(layout="wide")

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


@st.dialog("Add Vinyl")
def add_vinyl():
    global vinyl_list
    name = st.text_input("Title of vinyl")
    picture_link = st.text_input("URL of a picture of the album cover")
    if st.button("Add to collection") and name is not None and picture_link is not None:
        vinyl_names.append(name.strip())
        vinyl_pictures.append(picture_link.strip())
        vinyl_list = dict(zip(vinyl_names, vinyl_pictures))


st.title("Vinyls", text_alignment="center")
st.space("medium")
with st.container(horizontal=True, horizontal_alignment="center"):
    for vinyl in vinyl_list:

        @st.dialog(f"{vinyl}")
        def vinyl_display():
            st.image(vinyl_list[vinyl], width=500)
            st.text(f"Album name: {vinyl}", text_alignment="center")

        with st.container(width="content", horizontal_alignment="left"):
            st.image(vinyl_list[vinyl], width=200)
            if st.button(f"{vinyl}", width=200):
                vinyl_display()

with st.container(horizontal=True, horizontal_alignment="right", vertical_alignment="bottom"):
    if st.button("Add Vinyl"):
        add_vinyl()
        # add_vinyl does not currently work, permament additions to the list
        # in a collection will have to be done on the database side, so
        # this is a temporary wall