from mindee import Client, documents
import json


class RecipeParsingError(Exception):
    def __init__(self, filename, text="Couldn't parse the recipe"):
        self.filename = filename
        self.text = text
        super().__init__(text)


def recipe_to_dict(filename, api_key_str):
    client = Client(api_key=api_key_str)
    input_doc = client.doc_from_path(filename)
    result = input_doc.parse(documents.TypeReceiptV5).document

    shop = result.supplier_name
    total = result.total_amount.value
    date = result.date.date_object
    time = result.time
    if str(shop) == "" or total is None or date is None or str(time) == "":
        raise RecipeParsingError(filename)

    recipe_data = {
        "shop": str(shop),
        "total": float(total),
        "date": date.strftime("%d/%m/%Y") + ", " +\
            str(time),
    }

    return recipe_data

def save_recipe_from_image(filename, api_key_filename):

    with open(api_key_filename, "r") as f:
        key = f.read()

    with open("recipes.json") as f:
        data = json.load(f)

    recipe_dict = recipe_to_dict(filename, key)
    recipe_json = recipe_dict

    data.append(recipe_json)

    with open("recipes.json", "w") as f:
        json.dump(data, f, indent=4)



try:
    save_recipe_from_image("C:/Users/Michał/Desktop/recipes/paragon1.png", "key.txt")
except RecipeParsingError as inst:
    print(f"{inst.text}: {inst.filename}")
except FileNotFoundError:
    print(f"Coudn't find one of the files")
