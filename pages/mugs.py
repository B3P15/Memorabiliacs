import streamlit as st
import global_functions as gfuncs

st.set_page_config(layout="wide")

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

@st.dialog("Add Mug")
def add_mug():
    st.text("We're working on this feature!")
    #global mug_list
    #name = st.text_input("Title of vinyl")
    #picture_link = st.text_input("URL of a picture of the album cover")
    #if st.button("Add to collection") and name is not None and picture_link is not None:
    #    mug_names.append(name.strip())
    #    mug_pictures.append(picture_link.strip())
    #    mug_list = dict(zip(mug_names, mug_pictures))


st.title("Mugs", text_alignment="center")
st.space("medium")
with st.container(horizontal=True, horizontal_alignment="center"):
    for mug in mug_list:

        @st.dialog(f"{mug}")
        def mug_display():
            st.image(mug_list[mug], width=500)
            st.text(f"Mug name: {mug}", text_alignment="center")

        with st.container(width="content", horizontal_alignment="left"):
            st.image(f"pictures/{mug_list[mug]}.jpeg", width=150)
            if st.button(f"{mug}", width=150):
                mug_display()

with st.container(horizontal=True, horizontal_alignment="right", vertical_alignment="bottom"):
    if st.button("Add Mug"):
        add_mug()