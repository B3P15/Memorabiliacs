import streamlit as st
#basic method that grabs from mysql database to query a collection to determine what the user has
def gatherCollectionData(user:str):
    conn = st.connection('mysql', type='sql')
    #use st.connection.execute for inserting values into tables and whatnot
    collectionDF = conn.query('select A.* from aruppdb.pokemon as A; ') # This query is just an example to show how we can dynamically call information
    return collectionDF

# def addToCollection()

def removeCollection(tableName:str):
    #This command is dangerous. Ensure that proper On Delete cascade is implemented
    pass

def addCollection(tableName:str):
    conn = st.connection('mysql', type='sql')
    conn.session.execute(f'CREATE TABLE {tableName} column1 datatype constraints, column2 datatype constraints, ...);')
#Once the database is structured how we intend to use it, more methods cna be written to gather exactly the information that we want and format it.