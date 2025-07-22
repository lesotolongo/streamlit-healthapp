import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

#Lester Sotolongo
#Human-Computer Interaction CAP4104
#Class Project: UI/UX Design with Streamlit

# API details for Exercise
EXERCISE_API_HOST = "exercisedb.p.rapidapi.com"
EXERCISE_API_KEY = "2aaf684721msh636aac02ab83f5bp194eb6jsn2ee3bdca391d"

# API details for Nutrition
NUTRITION_API_URL = "https://food-nutrition-information.p.rapidapi.com/foods/search"
NUTRITION_API_HEADERS = {
    "X-RapidAPI-Host": "food-nutrition-information.p.rapidapi.com",
    "X-RapidAPI-Key": "2aaf684721msh636aac02ab83f5bp194eb6jsn2ee3bdca391d"
}

# Helper function for fetching exercises
def fetch_exercises_by_muscle_group(muscle_group):
    url = f"https://{EXERCISE_API_HOST}/exercises/target/{muscle_group}"
    headers = {
        "X-RapidAPI-Key": EXERCISE_API_KEY,
        "X-RapidAPI-Host": EXERCISE_API_HOST
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data from the API. Please check your API key or endpoint.")
        return []

# Main app structure
st.title(":rainbow[Physical & Nutrition Wellness Guide]")

# Sidebar Navigation
st.sidebar.header(":rainbow[Select your Wellness Guide:]")
app_selection = st.sidebar.radio("Select your Guide:", ["Nutrition Wellness", "Exercise Wellness"])

if app_selection == "Exercise Wellness":
    st.sidebar.title(":gray[Exercise Wellness]")
    st.sidebar.header(":red[Choose a Guide]")

    option = st.sidebar.radio(
        "Select an option:",
        ("Show Exercises", "Muscle Mass Loss")
    )

    if option == "Muscle Mass Loss":
        st.header(":orange[Average Muscle Mass Loss with Age]")
        st.write("The following data shows an average percentage of muscle mass loss for adults over the age of 50.  "
                 "Target these muscles for better overall health.")

        # Muscle loss data
        muscle_loss_data = {
            "Muscle": ["Psoas (Hip Flexor)", "Quadriceps (Thigh)", "Deep Back Muscles", "Triceps (Upper Arm)",
                       "Biceps (Upper Arm)", "Hamstrings (Thigh)", "Calf", "Glutes", "Ankle/Shin"],
            "Loss (%)": [29, 27, 24, 20, 19, 19, 14, 13, 9]
        }
        df = pd.DataFrame(muscle_loss_data)

        col1, col2 = st.columns(2)

        with col1:
            fig, ax = plt.subplots()
            ax.plot(df["Muscle"], df["Loss (%)"], marker='o', linestyle='-')
            ax.set_title("Average Muscle Mass Loss for Adults 50+ ")
            ax.set_ylabel("Loss (%)")
            ax.set_xlabel("Muscle Group")
            ax.set_xticklabels(df["Muscle"], rotation=45, ha="right")
            st.pyplot(fig)

        with col2:
            st.dataframe(df)

    elif option == "Show Exercises":
        st.sidebar.header(":red[Select a Muscle Group]")
        muscle_groups = [
            "abductors", "abs", "biceps", "calves", "cardiovascular system", "delts",
            "forearms", "glutes", "hamstrings", "lats", "levator scapulae", "pectorals",
            "quads", "serratus anterior", "spine", "traps", "triceps", "upper back"
        ]
        selected_muscle_group = st.sidebar.selectbox("Muscle Group", muscle_groups)

        if st.sidebar.button("Show Exercises"):
            st.header(f"Exercises for: :blue[{selected_muscle_group.capitalize()}]")
            exercises = fetch_exercises_by_muscle_group(selected_muscle_group)
            st.divider()

            if exercises:
                for exercise in exercises:
                    st.subheader(exercise["name"].capitalize())
                    st.write(f"**Equipment:** {exercise['equipment'].capitalize()}")
                    st.image(exercise["gifUrl"], width=300)
                    st.divider()
            else:
                st.write("No exercises found.")

elif app_selection == "Nutrition Wellness":
    st.sidebar.title(":green[Nutrition Information]")
    query = st.sidebar.text_input("Enter a food item (any food item... salad, mac and cheese, beef stew, etc.):")

    if st.sidebar.button("Search"):
        if query:
            params = {"query": query}
            response = requests.get(NUTRITION_API_URL, headers=NUTRITION_API_HEADERS, params=params)

            if response.status_code == 200:
                data = response.json()
                foods = data.get("foods", [])

                if foods:
                    food = foods[0]

                    st.subheader(f":green[Nutritional Data for: {food['description']}]")
                    nutrients = {nutrient["nutrientName"]: nutrient["value"] for nutrient in food["foodNutrients"]}

                    calories = nutrients.get("Energy", 0)
                    protein = nutrients.get("Protein", 0)
                    fat = nutrients.get("Total lipid (fat)", 0)
                    carbs = nutrients.get("Carbohydrate, by difference", 0)

                    col1, col2, col3, col4 = st.columns(4)
                    col1.write(f"**Total Calories:** {calories} kcal")
                    col2.write(f"**Protein:** {protein} g")
                    col3.write(f"**Fat:** {fat} g")
                    col4.write(f"**Carbohydrates:** {carbs} g")

                    labels = ["Protein", "Fat", "Carbohydrates"]
                    values = [protein, fat, carbs]

                    with st.expander("See Explanation"):
                        st.write(":blue[PROTEIN:] Proteins are made up of chemical 'building blocks' called amino acids. "
                                 "Your body uses amino acids to build and repair muscles and bones and to make hormones and enzymes.")
                        st.write(":blue[FAT:] Your body needs healthy fats for energy and other functions. "
                                 "But too much saturated fat can cause cholesterol to build up in your arteries (blood vessels).")
                        st.write(":blue[CARBS:] Carbohydrates include essential nutrients like sugars, starches, and fiber. "
                                 "Your body uses carbs to make glucose (blood sugar) for energy.")
                        st.write(":blue[CALORIES:] The amount of energy in food or drink is measured in calories. "
                                 "You need energy from calories for your body to work properly")

                    fig, ax = plt.subplots()
                    ax.pie(values, labels=labels, autopct="%2.0f%%", startangle=180)
                    ax.axis("equal")
                    st.pyplot(fig)

                else:
                    st.error("No nutritional data found for the specified food item.")
            else:
                st.error(f"API Error: {response.status_code}. Please try again later.")
        else:
            st.warning("Please enter a food item to search.")
