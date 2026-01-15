import streamlit as st
from collectionAPI import gatherCollectionData
from apitcg import get_cards
from apitcg2 import get_cards2
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

# id_list = []

# for i in range(4):
#     id_list.append(gatherCollectionData("2").loc[i, 'CardID'])
id_list = ["base1-3", "base3-15", "bw8"]
response = get_cards2("pokemon", id_list[0])
for j in range(20):
    st.image(response[j])
# print(id_list)
# # cardnum_list = ["3", "15", "8"]

# card_list = []
# #Ideally, using a correct table name and associated userid, this would generate the entire pokemon collection (including the unwanted info)
# #gatherCollectionData("Pokemon", 223)
# image_list = []
# for i in range(3):
#     card_dict = get_cards("pokemon", f"{id_list[i]}")["data"][0]
#     card_list.append("HP: "+card_dict["hp"]+"  \n"+"Type: "+card_dict["types"][0])
#     image_list.append(card_dict["images"]["small"])#
# for i in range(0, len(image_list), 3):
#     cols = st.columns(3)
#     j = 0
#     for col in cols:
#         col.image(image_list[j], width="content", caption=card_list[j])
#         j+=1