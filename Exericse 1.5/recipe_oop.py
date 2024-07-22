class Recipe:

    all_ingredients = set()

    def __init__(self,name):
        self.name = name
        self.ingredients = []
        self.cooking_time = int(0)
        self.difficutly = None

    def calculate_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = "easy"
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = "medium"
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = "intermediate"
        elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
            self.difficulty = "hard"

        return self.difficulty
    
    def getName(self):
        return self.name
    def setname(self, NewName):
        self.name = NewName
        return self.name
    
    def getCooking_time(self):
        return self.cooking_time
    def setCookingTime(self, SetCookingTime):
        self.cooking_time = SetCookingTime
        return self.cooking_time
    
    def getIngredients(self):
        return self.ingredients
    def AddIngredient(self, *NewIngredients):
        self.ingredients.extend(NewIngredients)
        self.update_all_ingredients()
    
    def getDifficulty(self):
        if self.difficutly is None:
            self.difficutly = self.calculate_difficulty()
        return self.difficulty
    
    def search_ingredient(self, ingredient):
        if ingredient in self.ingredients:
            return True
        else:
            return False
        
    def update_all_ingredients(self):
        for ele in self.ingredients:
            if ele not in self.all_ingredients:
                self.all_ingredients.add(ele)
        
        return self.all_ingredients
    
    def __str__(self):
            output = (
            "Name: "
            + self.name
            + "\nCooking Time (in minutes): "
            + str(self.cooking_time)
            + "\nIngredients: "
            + str(self.ingredients)
            + "\nDifficulty: "
            + str(self.difficutly)
            + "\n--------------------------"
            )
            return output
    
    def recipe_search(data, search_term):
        data = recipes_list
        for recipe in data:
            if recipe.search_ingredient(search_term) == True:
                print(recipe)
            
recipes_list = []

tea = Recipe("Tea")
tea.AddIngredient("Water", "Tea Leaves", "Sugar")
tea.setCookingTime(5)
tea.getDifficulty()

recipes_list.append(tea)

coffee = Recipe("Coffee")
coffee.AddIngredient("Coffee powder", "Water", "Milk")
coffee.setCookingTime(5)
coffee.getDifficulty()

recipes_list.append(coffee)

cake = Recipe("Cake")
cake.AddIngredient("Flour", "Sugar", "Eggs", "Milk", "Butter", "Vanilla Essence")
cake.setCookingTime(50)
cake.getDifficulty()

recipes_list.append(cake)

bannana_smoothie = Recipe("Bannana Smoothie")
bannana_smoothie.AddIngredient("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
bannana_smoothie.setCookingTime(5)
bannana_smoothie.getDifficulty()

recipes_list.append(bannana_smoothie)

print("Recipes List")
print("--------------------------")

for recipe in recipes_list:
    print(recipe)

print("Results for recipe_search with Water: ")
print("--------------------------")
Recipe.recipe_search(recipes_list, "Water")

print("Results for recipe_search with Sugar: ")
print("--------------------------")
Recipe.recipe_search(recipes_list, "Sugar")

print("Results for recipe_search with Bananas: ")
print("--------------------------")
Recipe.recipe_search(recipes_list, "Bananas")

