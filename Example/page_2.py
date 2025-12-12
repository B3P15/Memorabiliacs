import streamlit as st

st.title("Hello Streamlit-er 👋")
st.markdown(
    """ 
    This is page 2
    """
)

if st.button("Send balloons!"):
    st.balloons()