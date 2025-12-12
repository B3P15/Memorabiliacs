import streamlit as st

st.title("Hello Streamlit-er 👋")
st.markdown(
    """ 
    This is page 3
    """
)

if st.button("Send balloons!"):
    st.balloons()