import json
from pathlib import Path

data_dir = Path(r"C:\Users\andre\OneDrive\Desktop\Memorabilics\Memorabiliacs\BackendMethods\Pokemon_Cards")  # ← change this

pokemon_set = []  # use a set to auto-deduplicate

for json_file in data_dir.glob("*.json"):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for card in data:
        if "nationalPokedexNumbers" in card:
            card_id = card["id"]
            # card_name = card["name"]
            pokemon_set.append(card_id)

# Convert to sorted list if you want consistency
pokemon_list = sorted(pokemon_set)


def chunk_pokemon(pokemon_list, chunk_size=995):
    return [
        pokemon_list[i:i + chunk_size]
        for i in range(0, len(pokemon_list), chunk_size)
    ]

List = chunk_pokemon(pokemon_list, 995)

print(List[0])

print(List[0].index("bw11-22"))