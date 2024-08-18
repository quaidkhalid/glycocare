import anthropic
import streamlit as st

api_key = st.secrets["api_key"]


# Function to call the Anthropic API and get a meal suggestion
def get_meal_suggestion(api_key, fasting_sugar, pre_meal_level, post_meal_level, prepared_meal):
    client = anthropic.Anthropic(api_key=api_key)
    
    # Create a message with the user's input
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=500,
        temperature=0.9,
        system="You are a renowned clinical nutritionist specializing in diabetes management. Based on the user's current blood sugar levels (fasting, pre-meal, and post-meal) and the provided meal description, recommend a nutritionally balanced and diabetes-friendly meal. Ensure your suggestion supports optimal glycemic control and overall well-being.",
        messages=[
            {
                "role": "user",
                "content": f"My fasting sugar level is {fasting_sugar} mg/dL, pre-meal sugar level is {pre_meal_level} mg/dL, post-meal sugar level is {post_meal_level} mg/dL, and the meal I prepared is {prepared_meal}. Can you suggest a meal?"
            }
        ]
    )

    # Return the suggested meal
    raw_context = message.content
    itinerary = raw_context[0].text
    return itinerary

# Streamlit app setup
st.title('GlucoCare')

# App description
st.write("""
**GlucoCare** is your companion for managing blood sugar levels effectively. 
This app allows you to track your fasting, pre-meal, and post-meal sugar levels 
and provides meal suggestions based on your inputs. Stay on top of your health with GlucoCare.
""")

# Sidebar for input fields
st.sidebar.header('Input Your Data')

# Input fields
fasting_sugar = st.sidebar.number_input('Fasting Sugar Level (mg/dL)', min_value=0.0, format="%.1f")
pre_meal_level = st.sidebar.number_input('Pre-Meal Sugar Level (mg/dL)', min_value=0.0, format="%.1f")
post_meal_level = st.sidebar.number_input('Post-Meal Sugar Level (mg/dL)', min_value=0.0, format="%.1f")
prepared_meal = st.sidebar.text_input('Prepared Meal Description')

# Display the inputs for user verification
st.subheader('Your Inputs:')
st.write(f"**Fasting Sugar Level:** {fasting_sugar} mg/dL")
st.write(f"**Pre-Meal Sugar Level:** {pre_meal_level} mg/dL")
st.write(f"**Post-Meal Sugar Level:** {post_meal_level} mg/dL")
st.write(f"**Prepared Meal Description:** {prepared_meal}")

# Button to get meal suggestion
if st.button("Get Meal Suggestion"):
    # Call the function to get a meal suggestion
    suggested_meal = get_meal_suggestion(api_key, fasting_sugar, pre_meal_level, post_meal_level, prepared_meal)
    
    # Display the suggested meal
    st.subheader('Suggested Meal:')
    st.write(suggested_meal)
