import pickle

def calc_difficulty(recipe):
    if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
        x = "easy"

    elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
        x = "medium"

    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
        x = "intermediate"

    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) >= 4:
        x = "hard"

    return x

def take_recipe():
    name = str(input("Enter the name of your recipe: "))
    cooking_time = int(input("Enter the time is takes to cook: "))
    ingredients = list(input("Enter each of your ingredients with each seperated by comma: ").split(", "))
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients
    }

    recipe['difficulty'] = calc_difficulty(recipe)

    return recipe


filename = input("Enter the filename where you've stored your recipes: ")

try:
   file = open(filename, "rb")
   data = pickle.load(file)

except FileNotFoundError:
    print("file not found, creating a new recipe file")
    data = {"recipes_list": [], "all_ingredients": []}
except:
    print("Something is wrong, creating a new recipe file")
    data = {"recipes_list": [], "all_ingredients": []}
    
else:
    file.close()

finally:
    recipes_list = data["recipes_list"]
    all_ingredients = data["all_ingredients"]

numberOfRecipies = int(input("How many recipes would you like to enter:"))

for i in range(numberOfRecipies):
    recipe = take_recipe()
    recipes_list.append(recipe)

    for element in recipe["ingredients"]:
        if not element in all_ingredients:
            all_ingredients.append(element)

    print("recipe added successfully")

data = {"recipes_list": recipes_list, "all_ingredients": all_ingredients}

newfile = open(filename, "wb")
pickle.dump(data, newfile)

newfile.close()
print("Your recipes have been changed")