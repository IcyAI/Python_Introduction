
import mysql.connector

conn = mysql.connector.connect(
        host='localhost',
        user='cf-python',
        passwd='password',
    )
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS new_task_database")

cursor.execute("USE new_task_database")

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50),
                ingredients VARCHAR(250),
                cooking_time INT,
                difficulty VARCHAR(20)
                )''')

def calculate_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        return "easy"
    elif cooking_time < 10 and len(ingredients) >= 4:
        return "medium"
    elif cooking_time >= 10 and len(ingredients) < 4:
        return "intermediate"
    elif cooking_time >= 10 and len(ingredients) >= 4:
        return "hard"

def create_recipe(conn, cursor):
    name = input("Enter the name of your recipe: ")
    cooking_time = int(input("Enter cooking time (in minutes): "))
    ingredients = input("Enter ingredients (separated by a comma): ").split(",")
    difficulty = calculate_difficulty(cooking_time, ingredients)
    ingredients_str = ", ".join(ingredients).strip()

    sql = "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
    val = (name, ingredients_str, cooking_time, difficulty)

    cursor.execute(sql, val)
    conn.commit()
    print("Recipe saved in database.")

def search_recipe(conn, cursor):
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()

    all_ingredients = []
    for row in results:
        all_ingredients.extend(row[0].split(","))

    unique_ingredients = list(set(all_ingredients))

    print("Available ingredients:")
    for index, ingredient in enumerate(unique_ingredients):
        print(f"{index}: {ingredient}")

    search_ingredient_number = int(input("Enter a number corresponding to an ingredient to search for: "))
    search_ingredient = unique_ingredients[search_ingredient_number]

    cursor.execute("SELECT * FROM recipes WHERE ingredients LIKE %s", ("%" + search_ingredient + "%",))
    results = cursor.fetchall()

    for recipe in results:
        print("\nRecipe ID:", recipe[0])
        print("Name:", recipe[1])
        print("Ingredients:", recipe[2])
        print("Cooking time:", recipe[3], "minutes")
        print("Difficulty:", recipe[4])

    conn.commit()

def update_recipe(conn, cursor):
    cursor.execute("SELECT * FROM Recipes")
    for row in cursor:
        print(row)

    selection = int(input("Select a recipe ID to update: "))
    print("1. Name")
    print("2. Cooking time")
    print("3. Ingredients")

    col_selection = int(input("Select a column to update: "))

    if col_selection == 1:
        new_name = input("Enter a new name for the recipe: ")
        sql = "UPDATE recipes SET name = %s WHERE id = %s"
        val = (new_name, selection)
        cursor.execute(sql, val)
        conn.commit()
        print("Recipe updated successfully.")

    elif col_selection == 2:
        new_cooking_time = int(input("Enter a new cooking time (in minutes): "))
        sql = "UPDATE recipes SET cooking_time = %s WHERE id = %s"
        val = (new_cooking_time, selection)
        cursor.execute(sql, val)
        conn.commit()

        cursor.execute("SELECT ingredients FROM recipes WHERE id = %s", (selection,))
        result = cursor.fetchone()
        current_ingredients = result[0]  

        new_difficulty = calculate_difficulty(new_cooking_time, current_ingredients.split(","))

        sql = "UPDATE recipes SET difficulty = %s WHERE id = %s"
        val = (new_difficulty, selection)
        cursor.execute(sql, val)
        conn.commit()
        print("Recipe and difficulty updated successfully.")

    elif col_selection == 3:
        new_ingredients = input("Enter ingredients (separated by a comma): ")

        sql = "UPDATE recipes SET ingredients = %s WHERE id = %s"
        val = (new_ingredients, selection)
        cursor.execute(sql, val)

        cursor.execute("SELECT cooking_time FROM recipes WHERE id = %s", (selection,))
        result = cursor.fetchone()
        current_cooking_time = result[0]

        new_difficulty = calculate_difficulty(current_cooking_time, new_ingredients.split(","))

        sql = "UPDATE recipes SET difficulty = %s WHERE id = %s"
        val = (new_difficulty, selection)
        cursor.execute(sql, val)
        conn.commit()
        print("Recipe and difficulty updated successfully.")

    else:
        print("Invalid input, please try again.")

def delete_recipe(conn, cursor):
    cursor.execute("SELECT * FROM Recipes")
    for row in cursor:
        print(row)

    selection = int(input("Select a recipe ID to delete: "))
    sql = "DELETE FROM recipes WHERE id = %s"
    val = (selection,)
    cursor.execute(sql, val)
    conn.commit()
    print("Recipe deleted successfully.")

def main_menu(conn, cursor):

    while True:
        choice = input("Choose an option:\n1. Create a recipe\n2. Search a recipe\n3. Update a recipe\n4. Delete a recipe\n5. Quit and Save\n")

        if choice == "1":
            create_recipe(conn, cursor)
        elif choice == "2":
            search_recipe(conn, cursor)
        elif choice == "3":
            update_recipe(conn, cursor)
        elif choice == "4":
            delete_recipe(conn, cursor)
        elif choice == "5":
            cursor.execute("SELECT * FROM recipes")
            everything = cursor.fetchall()
            for recipe in everything:
                print("\nRecipe ID:", recipe[0])
                print("Name:", recipe[1])
                print("Ingredients:", recipe[2])
                print("Cooking time:", recipe[3], "minutes")
                print("Difficulty:", recipe[4])
            break
        else:
            print("Invalid choice, please try again.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main_menu(conn, cursor)
