import csv
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
import json

# Function to get user data
def get_user_data():
    name = input("Enter your name: ")
    age = input("Enter your age: ")
    weight = float(input("Enter your weight (in kgs): "))
    height = float(input("Enter your height (in cms): "))
    return {"name": name, "age": age, "weight": weight, "height": height,}


# Function to save user data to JSON file
def save_user_data(data):
    with open('user_data.json', 'w') as f:
        json.dump(data, f)

# Function to load user data from JSON file
def load_user_data():
    with open('user_data.json') as f:
        return json.load(f)

# Function to prompt user to log in or sign up
def login_or_signup():
    choice = input("Enter 1 to log in or 2 to sign up: ")
    if choice == "1":
        # Log in
        while True:
            try:
                user_data = load_user_data()
            except FileNotFoundError:
                print("No user data found. Please sign up first.")
                return login_or_signup()
            name = input("Enter your name: ")
            age = input("Enter your age: ")
            if name == user_data['name'] and age == user_data['age']:
                print("Login successful!")
                return user_data
            else:
                print("Login failed. Please try again.")
    elif choice == "2":
        # Sign up
        user_data = get_user_data()
        save_user_data(user_data)
        print("Sign up successful!")
        return user_data
    else:
        print("Invalid choice. Please try again.")
        return login_or_signup()

# Get user data
user_data = login_or_signup()

# Create a function to log a workout session
def log_workout(user_data):
    # Get today's date
    date = datetime.today().strftime("%Y-%m-%d")

    # Ask the user for workout details
    exercise = input("Enter the exercise name: ")
    sets = int(input("Enter the number of sets: "))
    reps = int(input("Enter the number of reps per set: "))
    duration = float(input("Enter the duration of the exercise (in minutes): "))
    calories_burned = float(input("Enter the number of calories burned during the exercise: "))

    # Save the workout data to a CSV file
    with open(f"{user_data['name']}_workouts.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, exercise, sets, reps, duration, calories_burned])

    print("Workout logged successfully!")

# Create a function to generate monthly workout summary chart
def generate_monthly_workout_summary_chart(user_data):
    # Prompt user for the month
    month = input("Enter the month for which you want to generate the workout summary chart (format: mm-yyyy): ")

    # Create a dictionary to store monthly workout data
    monthly_data = defaultdict(float)

    # Read the workout data from the CSV file for the given month
    with open(f"{user_data['name']}_workouts.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            date = row[0]
            if date.endswith(month):
                duration = float(row[4])
                monthly_data[date[0:10]] += duration

    # Generate the workout chart
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.plot(list(monthly_data.keys()), list(monthly_data.values()))
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Workout Duration (minutes)")
    ax.set_title(f"{month} Workout Summary")

    plt.show()


# Create a function to generate a pie chart of the most common exercises
def generate_exercise_chart(user_data):
    # Create a dictionary to store exercise data
    exercise_data = defaultdict(int)

    # Read the workout data from the CSV file
    with open(f"{user_data['name']}_workouts.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            exercise = row[1]
            exercise_data[exercise] += 1

    # Generate the chart
    labels = list(exercise_data.keys())
    values = list(exercise_data.values())
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title("Most Common Exercises")
    plt.show()


# Create a function to generate a bar chart of the total calories burned
def generate_calories_chart(user_data):
    # Prompt user for the month
    month = input("Enter the month for which you want to generate the workout summary chart (format: mm-yyyy): ")

    # Create a dictionary to store monthly calorie data
    monthly_calories = defaultdict(float)

    # Read the workout data from the CSV file
    with open(f"{user_data['name']}_workouts.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            date = row[0]
            if date.endswith(month):
                calories = float(row[5])
                monthly_calories[date[0:7]] += calories
            

    # Generate the chart
    x_values = list(monthly_calories.keys())
    y_values = list(monthly_calories.values())
    plt.bar(x_values, y_values)
    plt.xlabel("Month")
    plt.ylabel("Total Calories Burned")
    plt.title("Monthly Calories Burned Summary")
    plt.show()


# Main program loop
while True:
    print("\n---- Fitness Tracker ----")
    print("1. Log a workout")
    print("2. Generate monthly workout summary chart")
    print("3. Generate pie chart of overall common exercises")
    print("4. Generate bar chart of total calories burned(monthly)")
    print("5. Exit")
    choice = input("Enter your choice (1-5): ")

    if choice == "1":
        user_data = load_user_data()
        log_workout(user_data)
    elif choice == "2":
        user_data = load_user_data()
        generate_monthly_workout_summary_chart(user_data)
    elif choice == "3":
        user_data = load_user_data()
        generate_exercise_chart(user_data)
    elif choice == "4":
        user_data = load_user_data()
        generate_calories_chart(user_data)
    elif choice == "5":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
