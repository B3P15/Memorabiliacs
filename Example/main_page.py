import streamlit as st
from collectionAPI import gatherCollectionData
from apitcg import get_cards
from apitcg2 import get_cards2
from internetarch import search_internetarchive
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


image_list = search_internetarchive()

for i in image_list:
    st.image(i[0])
    st.write(i[1])

# id_list = ["base1-3", "base3-15", "bw8"]
# response = get_cards2("pokemon", id_list[0])
# for j in range(20):
#     st.image(response[j])
# print(id_list)
# # cardnum_list = ["3", "15", "8"]

