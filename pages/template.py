import streamlit as st
import temp_backend as db

if st.button("Home"):
    st.switch_page("pages/home_page.py")

st.title(db.current_coll, text_alignment="center")

st.set_page_config(layout="wide")


# temp hard code for vinyls
if (db.current_coll == "Vinyls"):
    @st.dialog("Add Vinyl")
    def add_vinyl():
        name = st.text_input("Title of vinyl")
        picture_link = st.text_input("URL of a picture of the album cover")
        if st.button("Add to collection") and name != '' and picture_link != '':
            db.vinyl_names.append(name.strip())
            db.vinyl_pictures.append(picture_link.strip())
            db.vinyl_list = dict(zip(db.vinyl_names, db.vinyl_pictures))
            # st.switch_page("pages/template.py")
            st.rerun()
        else:
            pass
    
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
                if st.button("Remove", key=f"remove_{vinyl}", width=200):
                    db.vinyl_names.remove(vinyl)
                    db.vinyl_pictures.remove(db.vinyl_list[vinyl])
                    db.vinyl_list = dict(zip(db.vinyl_names, db.vinyl_pictures))
                    st.switch_page("pages/template.py")

    with st.container(horizontal=True, horizontal_alignment="right", vertical_alignment="bottom"):
        if st.button(f"Add to {db.current_coll}"):
            add_vinyl()
            pass


# above but mugs
if (db.current_coll == "Mugs"):
    
    @st.dialog("Add Mug")
    def add_vinyl():
        st.subheader("We're working on it :)")
    #     name = st.text_input("Name of Mug")
    #     picture_link = st.text_input("URL of a picture of the mug")
    #     if st.button("Add to collection") and name != '' and picture_link != '':
            
    #         st.rerun()
    #     else:
    #         pass
    
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
                
    with st.container(horizontal=True, horizontal_alignment="right", vertical_alignment="bottom"):
        if st.button(f"Add to {db.current_coll}"):
            add_vinyl()
            pass

