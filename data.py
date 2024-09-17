import http.client
import json
import urllib.parse

from categories import CATEGORY_TO_ICON
from env import YELP_API_KEY


def main():
    with open("data.txt", "r") as f:
        place_names = [parse_line(line) for line in f.readlines()]
    place_names = [place_name for place_name in place_names if place_name]
    places = [get_place(place_name) for place_name in place_names]
    places_json = json.dumps(places, indent=2)
    with open("places.js", "w") as f:
        f.write("const places = ")
        f.write(places_json)


def get_place(place_name: str):
    base_url = "api.yelp.com"
    endpoint = "/v3/businesses/search"
    headers = {"Authorization": f"Bearer {YELP_API_KEY}"}
    params = {"term": place_name, "location": "New Orleans, LA", "limit": 1}
    query = urllib.parse.urlencode(params)
    conn = http.client.HTTPSConnection(base_url)
    try:
        conn.request("GET", f"{endpoint}?{query}", headers=headers)
        response = conn.getresponse()
        if response.status != 200:
            raise Exception(f"API request failed with status code {response.status}")
        data = json.loads(response.read().decode())
        if not data["businesses"]:
            print(f"No results found for {place_name}")
            return None
        business = data["businesses"][0]
        category = business["categories"][0]["title"]
        print(f"Matching {place_name} with {business['name']}")
        try:
            return {
                "id": business["id"],
                "name": business["name"],
                "latitude": business["coordinates"]["latitude"],
                "longitude": business["coordinates"]["longitude"],
                "image_url": business["image_url"],
                "icon": CATEGORY_TO_ICON[category],
                "url": business["url"],
                "categories": [
                    category["title"] for category in business["categories"]
                ],
                "price": business.get("price"),
                "display_address": "\n".join(business["location"]["display_address"]),
                "menu_url": business.get("menu_url"),
            }
        except KeyError as e:
            print(f"Failed to get data for {place_name}")
            print("Output", json.dumps(business, indent=2))
            print(e)
            return None
    finally:
        conn.close()


def parse_line(line: str) -> str | None:
    split = line.split("- ")
    if len(split) <= 1:
        return None
    line = split[0]
    # remove text in parentheses
    line = line.split("(")[0].strip()
    return line


if __name__ == "__main__":
    main()
