import streamlit as st
from collectionAPI import gatherCollectionData

st.title("Hello Streamlit-er 👋")
st.markdown(
    """ 
    This is a playground for you to try Streamlit and have fun. 

    **There's :rainbow[so much] you can build!**
    
    We prepared a few examples for you to get started. Just 
    click on the buttons above and discover what you can do 
    with Streamlit. 

    If I add text here lets see what happens
    """
)

if st.button("Send balloons!"):
    st.balloons()

#Ideally, using a correct table name and associated userid, this would generate the entire pokemon collection (including the unwanted info)
gatherCollectionData("Pokemon", 223)