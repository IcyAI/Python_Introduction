recipes_list = []
ingredients_list = []

def take_recipe():
    name = str(input("Enter the name of your recipe: "))
    cooking_time = int(input("Enter the time is takes to cook: "))
    ingredients = list(input("Enter each of your ingredients with each seperated by comma: ").split(", "))
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients
    }

    return recipe

n = int(input("Enter the number of recipies you want to enter: "))


for i in range(n):

    i += 1
    recipe = take_recipe()

    for ingredient in recipe["ingredients"]:
        if not ingredient in ingredients_list:
            ingredients_list.append(ingredient)
    
    recipes_list.append(recipe)

for recipe in recipes_list:

    if recipe["cooking_time"] < 10 and len(recipe["ingredient"]) < 4:
        recipe['difficulty'] = "easy"

    elif recipe["cooking_time"] < 10 and len(recipe["ingredient"]) >= 4:
        recipe['difficulty'] = "medium"

    elif recipe["cooking_time"] >= 10 and len(recipe["ingredient"]) < 4:
        recipe['difficulty'] = "intermediate"

    elif recipe["cooking_time"] >= 10 and len(recipe["ingredient"]) >= 4:
        recipe['difficulty'] = "hard"

for recipe in recipes_list:
    print("Recipe: " + recipe["name"])
    print("Cooking time (min): " + recipe["cooking_time"])
   
    for ingredient in recipe["ingredients"]:
        print(ingredient)

    print("Difficulty: " + recipe["difficulty"])

print("Ingredients avaliable across all recipes")
print("----------------------------------------")
ingredients_list.sort()

for ingredient in ingredients_list:
    print(ingredient)

    