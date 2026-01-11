import streamlit as st


#basic method that grabs
def gatherCollectionData(collection:str, user:int):
    conn = st.connection('mysql', type='sql')
    collectionDF = conn.query(f'select * from {collection} as C where C.id = {user};') # This query is just an example to show how we can dynamically call information
    for _, row in collectionDF.itertuples():
        st.write(row)


#Once the database is structured how we intend to use it, more methods cna be written to gather exactly the information that we want and format it.