import pickle

def display_recipe(recipe):
    print("Name:", recipe["name"])
    print("coking_time:", recipe["cooking_time"])
    print("ingredients:")
    for ingredient in recipe["ingredients"]:
        print(ingredient)
    print("difficulty:", recipe["difficulty"])

def search_ingredient(data):
    all_data = list(enumerate(data["all_ingredients"]))

    for ingredient in all_data:
        print(ingredient[0],ingredient[1])

    try:
        indexNumber = int(input("pick a number from the above list to select an ingredient: "))
        ingredient_searched = all_data[indexNumber][1]
        print("finding recipies with", ingredient_searched)
    except:
        print("number is not a valid input")
    else:
        for ele in data["recipes_list"]:
            if ingredient_searched in ele["ingredients"]:
                print("recipe name", ele["name"])

filename = str(input("Enter the name of the file that contains your recipe data: "))

try:
    file = open(filename, "rb")
    data = pickle.load(file)
    print("file Loaded")
except:
    print("file could not be found")
else:
    search_ingredient(data)
    file.close()
    