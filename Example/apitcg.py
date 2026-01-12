# main.py
from fastapi import FastAPI, Query, Path, HTTPException
import requests

BASE_API_URL = "https://apitcg.com/api"
API_KEY = "0e2f13f05b5fd140a8cc5eccb2abbc1dc72c9485b46a79c4b2dda9e9284100f4"  # change later

app = FastAPI()


# urls in format of 'https://apitcg.com/api/$GAME/cards?$ATTRIBUTE='


@app.get("/{game}/cards")
def get_cards(
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

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    return response.json()

