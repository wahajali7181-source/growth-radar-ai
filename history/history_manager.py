import json
import os


FILE_NAME = "data/search_history.json"


def load_history():

    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)


def save_search(business, city):

    history = load_history()

    history.insert(
        0,
        {
            "business": business,
            "city": city
        }
    )

    history = history[:20]

    with open(FILE_NAME, "w", encoding="utf-8") as f:

        json.dump(
            history,
            f,
            indent=4
        )