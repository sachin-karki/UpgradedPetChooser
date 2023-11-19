# Sachin Karki
# Assignment 11, Upgraded Pet Chooser
import mysql.connector  # Python Package to connect SQL to Python
from pet import Pet  # Importing Pet class from pet.py

print("Welcome to Pet Chooser Version 2.0!")  # Welcome Screen
# This defined function will help to load the database
def pet_database():
    global petDatabase, cursor
    pets = []  # This initializes an empty list to be used for displaying the list of pets
    try:
        # Setting the database parameters to connect to MySQL database
        petDatabase = mysql.connector.connect(
            host="localhost",
            user="root",
            password="0329724Rs!",
            database="pets"
        )
        cursor = petDatabase.cursor()  # Creating a cursor class to execute our query
        # Our SQL Query to be executed
        query = """  
        SELECT pets.id, pets.name, types.animal_type, pets.age, owners.name
        FROM pets
        JOIN types ON pets.animal_type_id = types.id
        JOIN owners ON pets.owner_id = owners.id;
        """
        cursor.execute(query)
        data = cursor.fetchall()
        for row in data:
            pet = Pet(*row)
            pets.append(pet)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        petDatabase.close()
    return pets

# This function will display the initial listing to the user as options to choose from
def print_pet_list(pet_list):
    print("Please Choose a Pet From the List Below::")
    for i, pet in enumerate(pet_list, start=1):
        print(f"[{i}] {pet.name}")
    print("[Q] Quit")

# This function will display the pet information you chose from the input along with some other information
def display_pet_info(pet):
    print(
        f"You have chosen {pet.name}, the {pet.animal_type}. {pet.name} is {pet.age} years old. {pet.name}'s owner is {pet.owner_name}.\n")

# This function will allows us the to edit pet information
def edit_pet(pet):
    print(f"You have chosen to edit {pet.name}.\n")
    new_name = input("New name: [ENTER == no change]: ")
    if new_name:
        pet.name = new_name
        print(f"The pet's name has been updated to {pet.name}.\n")

    new_age = input("New age: [ENTER == no change]: ")
    if new_age:
        try:
            pet.age = int(new_age)
            print(f"The pet's age has been updated to {pet.age}.\n")
        except ValueError:
            print("Invalid input. Age must be a number.\n")

# Loading the list of pets from the database
pet_list = pet_database()
while True:  # Setting up conditions for user input that corresponds correct pet information
    print_pet_list(pet_list)
    choice = input("Please Enter a Number From the List to Choose a Pet:")
    if choice.lower() == 'q':  # This will quit the program in the event q or Q is fed as an input
        print("Quitting the Program")
        break  # Stops the program
    try:
        choice = int(choice)
        if 1 <= choice <= len(pet_list):
            selected_pet = pet_list[choice - 1]
            display_pet_info(selected_pet)
            option = input("Would you like to [C]ontinue, [Q]uit, or [E]dit this pet?: ").upper()
            # The option input prompt above Will list new set of options

            if option == 'C':
                continue
            elif option == 'Q':
                break
            elif option == 'E':
                edit_pet(selected_pet)
            else:
                print("Invalid option. Please enter C, Q, or E.\n")
        else:
            print("Invalid Input. Please Select a Valid Pet Number as Shown in the List.\n")
    except EOFError:
        print("That's an Illegal Input. Please Enter a Legal One: \n")
    except ValueError:  # Prompts an error message if anything other than the input options is given
        print("Wrong Input Type. Please Enter a Valid Pet Number or 'Q/q' to Quit.")
