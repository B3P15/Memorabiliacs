# main.py
from fastapi import FastAPI, Query, Path, HTTPException
from requests_futures.sessions import FuturesSession
from concurrent.futures import as_completed

BASE_API_URL = "https://apitcg.com/api"
API_KEY = "5ac2e3910327e2774a197552796a62b1f14e6eb8992155b29cd6fc47f826ea87"  # change later

app = FastAPI()


# urls in format of 'https://apitcg.com/api/$GAME/cards?$ATTRIBUTE='

#Faster version of get_cards using asynchronous gets and future responses
@app.get("/{game}/cards")
def get_cards2(
    game: str = Path(..., description="Game type: one-piece, pokemon, yugioh, etc."),
    id: list[str] = Query(..., description="Card name(s) to search")
):
    url = f"{BASE_API_URL}/{game}/cards"

    headers = {
        "x-api-key": API_KEY
    }


    futureList = []

    responseList = []
    session = FuturesSession()
    # first request is started in background
    for i in range(len(id)-1):
        params = {
        "id": id[i]}
        futureList.append(session.get(url, headers=headers, params=params))
    for future in as_completed(futureList):
        #create the dictionary with the id, name, type, hp, and image url
        try:
            card_hp = future.result().json()["data"][0]["hp"]
        except (KeyError, TypeError):
            card_hp = 0
        try:
            card_text = future.result().json()["data"][0]["flavorText"]
        except (KeyError, TypeError):
            card_text = ""
        card_name = future.result().json()["data"][0]["name"]
        card_id = future.result().json()["data"][0]["id"]
        image_url = future.result().json()["data"][0]["images"]["small"]
        responseList.append({
            "id": card_id,
            "flavorText": card_text,
            "hp": card_hp,
            "name": card_name,
            "image": image_url
        })

    return(responseList)

