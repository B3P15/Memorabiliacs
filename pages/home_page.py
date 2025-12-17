import streamlit as st
import global_functions as gfuncs

collection_list = ['Pokemon Cards', 'Mugs', 'Movies', 'Video Games', 'Books', 'Vinyls']

collection_page_list = gfuncs.create_page_dict(collection_list)

st.title("Collections", text_alignment="center")
st.space("large")

with st.container(horizontal=True, horizontal_alignment="center"):

    for coll in collection_list:
        
        @st.dialog(f"{coll}")
        def collection_edit_display():
            st.text("We're working on it!")

        with st.container(width="content", horizontal_alignment="center"):
            st.subheader(f"{coll}", text_alignment="center")
            if st.button("View Collection", key=f"{coll}_link"):
                st.switch_page(f"pages/{collection_page_list[coll]}.py")
            if st.button("Edit", key=f"edit_{coll}"):
                collection_edit_display()

            st.space("medium")
        
        st.space("small")
