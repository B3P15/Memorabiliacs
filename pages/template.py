import streamlit as st
import temp_backend as db

st.title(db.current_coll, text_alignment="center")

st.set_page_config(layout="wide")


# temp hard code for vinyls
if (db.current_coll == "Vinyls"):
    with st.container(horizontal=True, horizontal_alignment="center"):
        for vinyl in db.vinyl_list:

            @st.dialog(f"{vinyl}")
            def vinyl_display():
                st.image(db.vinyl_list[vinyl], width=500)
                st.text(f"Album name: {vinyl}", text_alignment="center")

            with st.container(width="content", horizontal_alignment="left"):
                st.image(db.vinyl_list[vinyl], width=200)
                if st.button(f"{vinyl}", width=200):
                    vinyl_display()


# above but mugs
if (db.current_coll == "Mugs"):
    with st.container(horizontal=True, horizontal_alignment="center"):
        for mug in db.mug_list:

            @st.dialog(f"{mug}")
            def mug_display():
                st.image(db.mug_list[mug], width=500)
                st.text(f"Mug name: {mug}", text_alignment="center")

            with st.container(width="content", horizontal_alignment="left"):
                st.image(f"pictures/{db.mug_list[mug]}.jpeg", width=150)
                if st.button(f"{mug}", width=150):
                    mug_display()

