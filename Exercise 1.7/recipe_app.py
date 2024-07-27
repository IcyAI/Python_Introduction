#imports
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

# Initialize the engine with environment variables
DATABASE_URL = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

#initialize the base
Base = declarative_base()

#created session
Session = sessionmaker(bind=engine)
session = Session()

#create class, which also creates table since Base is inherited
class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    #repr method
    def __repr__(self):
        return "Recipe(ID=" + str(self.id) + ", Name='" + self.name + "', " \
            "Ingredients='" + self.ingredients 
       
    # general string print method
    def __str__(self):
        return (
            "----------\n"
            + "\tRecipe ID: " + str(self.id) + "\n"
            + "\tRecipe Name: " + self.name + "\n"
            + "\tRecipe Ingredients: " + self.ingredients + "\n"
            + "\tRecipe Cooking Time: " + str(self.cooking_time) + " minutes\n"
            + "\tRecipe Difficulty: " + self.difficulty + "\n"
            + "----------"
        )
    
    #calcualte_difficulty mehtod
    def calculate_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = "easy"
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = "medium"
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = "intermediate"
        elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
            self.difficulty =  "hard"
        else:
            print("difficulty can not be calculated, please try again")

    #Return ingredients as a string method
    def return_ingredients_as_list(self):
        if not self.ingredients:
            return []
        else:
            return list(self.ingredients.split(", "))
            

    
# Creates table in database
Base.metadata.create_all(engine)

#create recipe method
def create_recipe():

    #loop to input name and cooking time of recipe
    while(True):
        check = 0
        name = input("Enter the name of your recipe: ")
        cooking_time = input("Enter the amount of time in minutes it takes to cook: ")

        if(len(name) <= 20 and name.isalpha()):
            check = check + 1
        else:
            print("name is too long and/or name can not contain numbers")

        if (cooking_time.isnumeric()):
            check = check + 1
        else:
            print("cooking time can only contain numbers")

        if(check == 2):
            break
        else:
            print(check)
            print("please try to input the recipe information again")

    #temporty loop to input ingredients
    ingredients_list = []
    #number of ingredients to enter
    number_of_ingredients = int(input("Enter how many ingredients you want to input: "))

    #loop to enter ingredients
    for i in range(number_of_ingredients):
        ingredient = input("Enter one of your ingredients: ")
        ingredients_list.append(ingredient)

    #change ingredients into string
    ingredients = ", ".join(ingredients_list)

    #initalize recipe object
    recipe = Recipe (
        name = name,
        ingredients = ingredients,
        cooking_time = int(cooking_time)
    )

    #calculate difficulty of recipe object
    recipe.calculate_difficulty()

    #add to Recipe object to table
    session.add(recipe)

    #commit changes to table
    session.commit()

    #added new recipe
    print("recipe added to database")

#create view all recipe method
def view_all_recipes():

    #add all recipes to a list
    recipe_list = session.query(Recipe).all()

    #if list empty infor user stop function
    if recipe_list == []:
        print("Their are no recipes to print, add some recipes first")
        return None
    
    # else print all recipes
    else:
        for recipe in recipe_list:
            print(recipe)

# search recipe by ingredient method
def search_by_ingredients():

    #count the number of recipes in table 
    check = session.query(Recipe).count()

    #if 0 inform user and end function
    if check == 0:
        print("Their are no recipes add some first")
        return None
    
    #pull all ingredients from table
    results =  results = session.query(Recipe).all()

    #create ingredient list
    all_ingredients = []

    #adding ingredients to all_ingredients
    for recipe in results:
        temporty_list = recipe.return_ingredients_as_list()
        all_ingredients.extend(temporty_list)

    #remove duplicates in list
    all_ingredients_final = list(set(all_ingredients))

    #print list to user with number
    for ingredient in all_ingredients_final:
        print(all_ingredients_final.index(ingredient), ingredient)

    while(True):
        # user selects numbers
        Selection = input("type in the number coresponing to the ingredients you want to search for with spaces inbetween: ")
        #convert selection to list
        search_ingredients = list(map(int, Selection.split()))

        #check that numbers are valid
        x = 0
        for number in search_ingredients:
            if int(number) > len(all_ingredients) - 1 or int(number) < 0:
                print("number input is not an option, please try again")
                x = x + 1
        
        if x == 0:
            break
        

    # Create list of ingredients to search for
    search_ingredients = [all_ingredients_final[index] for index in search_ingredients]

    # Build query conditions
    conditions = [Recipe.ingredients.like(f"%{ingredient}%") for ingredient in search_ingredients]

    # Use `or_` to combine conditions if you want to match any of the ingredients
    final_recipes = session.query(Recipe).filter(or_(*conditions)).all()

    # Print each recipe
    if final_recipes:
        for recipe in final_recipes:
            print(recipe)
    else:
        print("No recipes found matching the criteria.")

#edit recipes method
def edit_recipe():

    #count the number of recipes in table 
    check = session.query(Recipe).count()

    #if 0 inform user and end function
    if check == 0:
        print("Their are no recipes add some first")
        return None
    
    #get all recipes
    results = session.query(Recipe).all()

    #print id and name
    for recipe in results:
        print(recipe.id, recipe.name)

    # select and confirm Selection
    while(True):

        Selection= int(input("select a recipe id to delete that recipe: "))

        record = session.query(Recipe).filter(Recipe.id == Selection).all()

        if record:
            break
        else:
            print("id is not valid, try again")

    #retrieve selected recipe
    recipe_to_edit = session.query(Recipe).filter(Recipe.id == Selection).one()

    print("----------")
    print("1 name", recipe_to_edit.name)
    print("2 cooking time", recipe_to_edit.cooking_time)
    print("3 ingredients", recipe_to_edit.ingredients)

    while(True):
        #input number to change value
        value = int(input("select a number corespoding to a value to change: "))

        if(value > 3 or value < 0):
            print("pleae type in a valid vnumber")

        else:
            break

    # change values based input
    if value == 1:
        #New name
        Newname = input("type in a new name of the recipe: ")
        #update Recipe
        session.query(Recipe).filter(Recipe.id == Selection).update({Recipe.name: Newname})
        session.commit()

    if value == 2:
        # new cooking time
        Newcookingtime = int(input("type in a new cooking time in minutes: "))
        #update Recipe
        session.query(Recipe).filter(Recipe.id == Selection).update({Recipe.cooking_time: Newcookingtime})

        session.commit()

    if value == 3:
        #temporty loop to input ingredients
        ingredients_list = []
        #number of ingredients to enter
        number_of_ingredients = int(input("Enter how many ingredients you want to input: "))

        #loop to enter ingredients
        for i in range(number_of_ingredients):
            ingredient = input("Enter one of your ingredients: ")
            ingredients_list.extend(ingredient)

        #change ingredients into string
        ingredients = ", ".join(ingredients_list)

        #update recipe
        session.query(Recipe).filter(Recipe.id == Selection).update({Recipe.ingredients:ingredients})      

        session.commit()

    #update difficulty

    NewRecipe = session.query(Recipe).filter(Recipe.id == Selection).one()

    Newdifficutly = NewRecipe.calculate_difficulty()

    session.query(Recipe).filter(Recipe.id == Selection).update({Recipe.difficulty: Newdifficutly})

    session.commit()

#Delete are recipe
def delete_recipe():

    #count the number of recipes in table 
    check = session.query(Recipe).count()

    #if 0 inform user and end function
    if check == 0:
        print("Their are no recipes add some first")
        return None

    #get all recipes
    results = session.query(Recipe).all()

    #print id and name
    for recipe in results:
        print(recipe.id, recipe.name)

    # select and confirm Selection
    while(True):

        Selection= int(input("select a recipe id to delete that recipe: "))

        record = session.query(Recipe).filter(Recipe.id == Selection).all()

        if record:
            break
        else:
            print("id is not valid, try again")

    #retrieve selected recipe
    recipe_to_delete = session.query(Recipe).filter(Recipe.id == Selection).all()

    #confirm to delete selected recipe
    print(" Are you sure you want to delete this recipe")

    print(recipe_to_delete)

    value = int(input("inputs 1 for yes and 2 for no: "))

    if value <= 1:
        recipe = session.query(Recipe).filter( Recipe.id == Selection).one()
        session.delete(recipe)
        session.commit()

        print("recipe deleted")

    if value >= 2:
        print("no recipes deleted")
        return None
    
def main_menu():

    while(True):

        #print out user options
        print("1. Create a new recipe")
        print("2. View all recipes")
        print("3. Search for recipes by ingredients")
        print("4. Edit a recipe")
        print("5. Delete a recipe")
        print("6. Quit")

        #user inputs selection
        Selection = int(input("Select a number conrresponding with a function: "))

        if Selection == 1:
            create_recipe()
        elif Selection == 2:
            view_all_recipes()
        elif Selection == 3:
            search_by_ingredients()
        elif Selection == 4:
            edit_recipe()
        elif Selection == 5:
            delete_recipe()
        elif Selection == 6:
            print("Quiting application, thank you")
            return None
        else:
            print("Something is wrong, try inputing a number again please")


main_menu()
            
    


        

        








