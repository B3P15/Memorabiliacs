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
    id: str = Query(..., description="Card name to search")
):
    url = f"{BASE_API_URL}/{game}/cards"

    headers = {
        "x-api-key": API_KEY
    }

    params = {
        "id": id
    }

    futureList = []

    responseList = []
    session = FuturesSession()
    # first request is started in background
    for i in range(20):
        futureList.append(session.get(url, headers=headers, params=params))
    for future in as_completed(futureList):
        responseList.append(future.result().json()["data"][0]["images"]["small"])

    return(responseList)


id_list = ["base1-3", "base3-15", "bw8"]
print(get_cards2("pokemon", id_list[0]))

