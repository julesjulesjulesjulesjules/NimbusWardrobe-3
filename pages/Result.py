import requests
import streamlit as st

from datetime import datetime

# https://arnaudmiribel.github.io/streamlit-extras/extras/switch_page_button/
from streamlit_extras.switch_page_button import switch_page

# import from ../Main.py
from Main import API_KEY_OPEN_WEATHER, CATEGORIES


# Get geolocation ID and weather data, then provide clothing recommendation
def get_weather_and_clothing(city):
    # Get the current hour in the 24-hour format
    current_hour = int(datetime.now().strftime("%H"))

    # OpenWeather API endpoint
    endpoint = "http://api.openweathermap.org"

    # Geolocation ID
    url_geocoding = endpoint + f"/geo/1.0/direct?q={city},CH&limit=5&appid={API_KEY_OPEN_WEATHER}"
    r1 = requests.get(url_geocoding)
    geocoding_data = r1.json()
    lat = geocoding_data[0]["lat"]
    lon = geocoding_data[0]["lon"]

    # Weather Data
    url_forecast = endpoint + f"/data/2.5/forecast?units=metric&lat={lat}&lon={lon}&appid={API_KEY_OPEN_WEATHER}"
    r2 = requests.get(url_forecast)
    weather = r2.json()
    weather_text = weather["list"][0]["weather"][0]["main"]
    weather_temp = weather["list"][0]["main"]["temp"]

    # Initialization of clothing recommendation variables
    # Reference: Course Content
    outerwear_items = ""
    topwear_items = ""
    layering_items = ""
    bottomwear_items = ""
    footwear_items = ""
    accessories = []  # Accessories as a list for easier use

    # Example clothing recommendation logic based on weather_temp and weather_text
    # Reference: Course Content
    if weather_temp < -10:  # first if for distinction of temperatire brackets
        if weather_text in [
            "Rain",
            "Thunderstorm",
            "Drizzle",
            "Snow",
        ]:  # If/else to see if Waterproof clothes are needed
            outerwear_items = ["Winter Jacket/Coat"]
            topwear_items = ["Long-Sleeve Shirt", "Long-Sleeve Blouse"]
            layering_items = ["Heavy Sweater", "Fleece/Thermal Layer"]
            bottomwear_items = ["Pants", "Jeans", "Insulated Pants"]
            footwear_items = ["Insulated Winter Boots"]
            accessories.extend(
                [
                    "Belt",
                    "Warm Scarf",
                    "Beanie",
                    "Insulated Winter Gloves/Mittens",
                    "Thermal Socks",
                    "Thermal Leggings/Tights",
                ]
            )
        else:
            outerwear_items = ["Winter Jacket/Coat"]
            topwear_items = ["Long-Sleeve Shirt", "Long-Sleeve Blouse"]
            layering_items = ["Heavy Sweater", "Fleece/Thermal Layer"]
            footwear_items = ["Pants", "Jeans"]
            footwear = ["Insulated Winter Boots"]
            accessories.extend(
                [
                    "Belt",
                    "Warm Scarf",
                    "Beanie",
                    "Insulated Winter Gloves/Mittens",
                    "Thermal Socks",
                    "Thermal Leggings/Tights",
                ]
            )

    elif -10 <= weather_temp < 0:
        if weather_text in [
            "Rain",
            "Thunderstorm",
            "Drizzle",
            "Snow",
        ]:  # If/else to see if Waterproof clothes are needed
            outerwear_items = ["Winter Jacket/Coat"]
            topwear_items = ["Long-Sleeve Shirt", "Long-Sleeve Blouse"]
            layering_items = ["Heavy Sweater", "Fleece/Thermal Layer"]
            bottomwear_items = ["Pants", "Jeans", "Insulated Pants"]
            footwear_items = ["Insulated Winter Boots"]
            accessories.extend(
                [
                    "Belt",
                    "Warm Scarf",
                    "Beanie",
                    "Insulated Winter Gloves/Mittens",
                    "Thermal Socks",
                    "Thermal Leggings/Tights",
                ]
            )
        else:
            outerwear_items = ["Winter Jacket/Coat"]
            topwear_items = ["Long-Sleeve Shirt", "Long-Sleeve Blouse"]
            layering_items = ["Heavy Sweater", "Fleece/Thermal Layer"]
            bottomwear_items = ["Pants", "Jeans"]
            footwear_items = ["Insulated Winter Boots"]
            accessories.extend(
                [
                    "Belt",
                    "Warm Scarf",
                    "Beanie",
                    "Insulated Winter Gloves/Mittens",
                    "Thermal Socks",
                    "Thermal Leggings/Tights",
                ]
            )

    elif 0 <= weather_temp < 5:
        if weather_text in [
            "Rain",
            "Thunderstorm",
            "Drizzle",
            "Snow",
        ]:  # If/else to see if Waterproof clothes are needed
            outerwear_items = ["Winter Jacket/Coat"]
            topwear_items = ["Long-Sleeve Shirt", "Long-Sleeve Blouse"]
            layering_items = ["Heavy Sweater", "Cardigan"]
            bottomwear_items = ["Pants", "Jeans", "Insulated Pants"]
            footwear_items = ["Insulated Winter Boots"]
            accessories.extend(
                [
                    "Belt",
                    "Warm Scarf",
                    "Beanie",
                    "Insulated Winter Gloves/Mittens",
                    "Thermal Socks",
                    "Thermal Leggings/Tights",
                ]
            )
        else:
            outerwear_items = ["Winter Jacket/Coat", "Wool Coat", "Parka"]
            topwear_items = ["Long-Sleeve Shirt", "Long-Sleeve Blouse"]
            layering_items = ["Heavy Sweater", "Cardigan"]
            bottomwear_items = ["Pants", "Jeans", "Insulated Pants"]
            footwear_items = ["Classic Boots"]
            accessories.extend(
                [
                    "Belt",
                    "Warm Scarf",
                    "Beanie",
                    "Standard Gloves/Mittens",
                    "Thermal Socks",
                    "Thermal Leggings/Tights",
                ]
            )

    elif 5 <= weather_temp < 10:
        if weather_text in [
            "Rain",
            "Thunderstorm",
            "Drizzle",
            "Snow",
        ]:  # If/else to see if Waterproof clothes are needed
            outerwear_items = ["Trench Coat", "Lightweight Down Jacket", "Softshell Jacket"]
            topwear_items = ["Long-Sleeve Shirt", "Long-Sleeve Blouse", "Long-Sleeve Dress"]
            layering_items = ["Heavy Sweater", "Cardigan", "Hoodie"]
            bottomwear_items = ["Pants", "Jeans", "Insulated Pants"]
            footwear_items = ["Insulated Winter Boots", "Classic Boots"]
            accessories.extend(
                [
                    "Belt",
                    "Warm Scarf",
                    "Beanie",
                    "Insulated Winter Gloves/Mittens",
                    "Thermal Socks",
                    "Thermal Leggings/Tights",
                ]
            )
        else:
            outerwear_items = ["Trench Coat", "Lightweight Down Jacket", "Softshell Jacket", "Leather Jacket"]
            topwear_items = ["Long-Sleeve Shirt", "Long-Sleeve Blouse", "Long-Sleeve Dress"]
            layering_items = ["Cardigan", "Hoodie", "Lightweight Sweater"]
            bottomwear_items = ["Pants", "Jeans"]
            footwear_items = ["Classic Boots", "Ankle Boots"]
            accessories.extend(["Belt", "Warm Scarf", "Standard Gloves/Mittens", "Thermal Socks"])

    elif 10 <= weather_temp < 20:
        if weather_text in [
            "Rain",
            "Thunderstorm",
            "Drizzle",
            "Snow",
        ]:  # If/else to see if Waterproof clothes are needed
            outerwear_items = ["Softshell Jacket", "Raincoat", "Windbreaker"]
            topwear_items = ["T-Shirt", "Short-Sleeve Blouse", "Short-Sleeve Dress"]
            layering_items = ["Cardigan", "Hoodie", "Lightweight Sweater"]
            bottomwear_items = ["Pants", "Jeans"]
            footwear_items = ["Ankle Boots", "Rubber Rain Boots"]
            accessories.extend(["Belt", "Light Scarf", "Socks"])
        else:
            outerwear_items = ["Leather Jacket", "Denim Jacket", "Windbreaker", "Blazer"]
            topwear_items = ["T-Shirt", "Short-Sleeve Blouse", "Short-Sleeve Dress"]
            layering_items = ["Cardigan", "Hoodie", "Lightweight Sweater"]
            bottomwear_items = ["Pants", "Jeans"]
            footwear_items = ["Ankle Boots", "Sneakers"]
            accessories.extend(["Belt", "Light Scarf", "Socks"])

    elif 20 <= weather_temp < 25:
        if weather_text in ["Rain", "Thunderstorm", "Drizzle"]:  # If/else to see if Waterproof clothes are needed
            outerwear_items = ["Raincoat"]
            topwear_items = ["T-Shirt", "Short-Sleeve Blouse", "Short-Sleeve Dress"]
            layering_items = []
            bottomwear_items = ["Jeans", "Capri Pants"]
            footwear_items = ["Sneakers", "Rubber Rain Boots"]
            accessories.extend(["Belt", "Socks"])
        else:
            outerwear_items = ["Denim Jacket", "Blazer"]
            topwear_items = ["T-Shirt", "Short-Sleeve Blouse", "Short-Sleeve Dress"]
            layering_items = []
            bottomwear_items = ["Jeans", "Capri Pants"]
            footwear_items = ["Sneakers", "Loafers", "Sandals"]
            accessories.extend(["Belt", "Socks"])

    elif 25 <= weather_temp < 30:
        if weather_text in ["Rain", "Thunderstorm", "Drizzle"]:  # If/else to see if Waterproof clothes are needed
            outerwear_items = ["Raincoat"]
            topwear_items = ["T-Shirt", "Short-Sleeve Blouse", "Short-Sleeve Dress", "Tank Top"]
            layering_items = []
            bottomwear_items = ["Shorts", "Skirt"]
            footwear_items = ["Sneakers"]
            accessories.extend(["Belt", "Cap", "Socks"])
        else:
            outerwear_items = []
            topwear_items = ["T-Shirt", "Short-Sleeve Blouse", "Short-Sleeve Dress", "Tank Top"]
            layering_items = []
            bottomwear_items = ["Shorts", "Skirt"]
            footwear_items = ["Sneakers", "Loafers", "Sandals"]
            accessories.extend(["Belt", "Cap", "Socks"])

    elif weather_temp >= 30:
        if weather_text in ["Rain", "Thunderstorm", "Drizzle"]:  # If/else to see if Waterproof clothes are needed
            outerwear_items = ["Raincoat"]
            topwear_items = ["T-Shirt", "Short-Sleeve Blouse", "Short-Sleeve Dress", "Tank Top"]
            layering_items = []
            bottomwear_items = ["Shorts", "Skirt"]
            footwear_items = ["Sneakers"]
            accessories.extend(["Belt", "Cap", "Socks"])
        else:
            outerwear_items = []
            topwear_items = ["T-Shirt", "Short-Sleeve Blouse", "Short-Sleeve Dress", "Tank Top"]
            layering_items = []
            bottomwear_items = ["Shorts", "Skirt"]
            footwear_items = ["Sandals"]
            accessories.extend(["Belt", "Cap"])

    # Additional accessories based on weather condition
    if weather_text == "Clear":
        if 6 <= current_hour <= 17:
            accessories.append("Sunglasses")

    elif weather_text in ["Rain", "Thunderstorm", "Drizzle"]:
        accessories.append("Umbrella")

    # Returning the results
    return (
        weather_text,
        weather_temp,
        outerwear_items,
        topwear_items,
        layering_items,
        bottomwear_items,
        footwear_items,
        accessories,
    )


# check if logged in
current_user_id = st.session_state.get("current_user_id", None)
if current_user_id is None:
    st.write("Please login first.")
    switch_page("Login")

# check if the city is provided
city_name = st.session_state.get("city_name", None)
if city_name is None:
    switch_page("Main")

# load up the db
db = st.session_state.get("db", None)
if db is None:
    switch_page("Main")


# Weather and Clothing Recommendations Page - Function to display the results page of the app
# Reference:
# - https://docs.streamlit.io/library/api-reference/text/st.title
# - https://docs.streamlit.io/library/api-reference/text/st.header
# - https://docs.streamlit.io/library/api-reference/write-magic/st.write
# - https://docs.streamlit.io/library/api-reference/text/st.subheader
# - https://docs.streamlit.io/library/api-reference/data/st.dataframe
# - https://docs.streamlit.io/library/api-reference/text/st.markdown
# - ChatGPT for Bulletpoints

# set the title of the results page in the Streamlit app
st.title("Recommendation")

# To check which recommended clothing items are present in the user's wardrobe and which are missing
(
    weather_text,
    weather_temp,
    outerwear_items,
    topwear_items,
    layering_items,
    bottomwear_items,
    footwear_items,
    accessories,
) = get_weather_and_clothing(city_name)

# To open a connection to the wardrobe database
(
    present_items,
    missing_items_both_genders,
    missing_items_one_gender,
    detailed_present_items,
) = db.check_wardrobe_for_items(
    current_user_id,
    {
        "Outerwear": outerwear_items,
        "Topwear": topwear_items,
        "Layering": layering_items,
        "Bottomwear": bottomwear_items,
        "Footwear": footwear_items,
        "Accessories": accessories,
    },
)

# Define a dictionary mapping weather conditions to emojis
if weather_text == "Clear":
    emoji = ":sunny:"
elif weather_text == "Rain":
    emoji = ":rain_cloud:"
elif weather_text == "Thunderstorm":
    emoji = ":lightning_cloud:"
elif weather_text == "Drizzle":
    emoji = ":rain_cloud:"
elif weather_text == "Snow":
    emoji = ":snow_cloud:"
else:
    emoji = ""

# To display the current weather conditions for the specified city
st.header(f"Weather in {city_name}: {emoji}")
st.write(f"Weather Condition: {weather_text}")
st.write(f"Temperature: {int(weather_temp)}°C")

# update the background image depending on the weather_text
if weather_text == "Clear":
    background_image_url = "https://source.unsplash.com/random?blue%20sky"
elif weather_text == "Rain":
    background_image_url = "https://source.unsplash.com/random?rain"
elif weather_text == "Thunderstorm":
    background_image_url = "https://source.unsplash.com/random?Thunderstorm"
elif weather_text == "Drizzle":
    background_image_url = "https://source.unsplash.com/random?drizzle%20weather"
elif weather_text == "Snow":
    background_image_url = "https://source.unsplash.com/random?snow"
else:
    background_image_url = "https://source.unsplash.com/random?weather"

# Background box
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url({background_image_url});
        background-size: cover;
    }}
    .block-container {{
        background: rgba(255, 255, 255, 0.8); /* White with 80% opacity */
        padding: 20px; /* Adjust padding as needed */
        border-radius: 10px; /* Optional: Add rounded corners */
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Recommendation section for items in the user's wardrobe
# Check if the DataFrame with present items is not empty
st.header("Suitable Items in Your Wardrobe:")
if not detailed_present_items.empty:  # Debugging line to check column names
    print(
        "DataFrame Columns:", detailed_present_items.columns
    )  # For debugging: to print the column names of the DataFrame to the console

    # List of categories to organize the displayed wardrobe items
    for category in CATEGORIES.keys():  # To loop through each category and display items under each
        st.subheader(f"{category}")
        df_category = detailed_present_items[
            detailed_present_items["category"] == category
        ]  # To filter and display items belonging to the current category
        if not df_category.empty:
            st.dataframe(df_category, hide_index= True)
            # To display the items in a table format
        else:
            st.write(
                f"No items found in {category} category."
            )  # To display message if no items are found in the category
else:
    st.write(
        "No specific items found in your wardrobe."
    )  # Message displayed if there are no suitable items found in the wardrobe

# Suggestion section for items (both genders) missing from the user's wardrobe
if missing_items_both_genders:
    st.header("Consider Purchasing the Following Items:")
    # Display message with suggested items that are not in the wardrobe but recommended for current weather
    st.write(
        "It seems that you don't own certain items that are recommended for these temperatures. "
        + "Consider acquiring the following pieces:"
    )
    bullet_points = "\n".join(
        [f"- {item}" for item in missing_items_both_genders]
    )  # To list the missing items in bullet points
    st.markdown(bullet_points, unsafe_allow_html=True)

# Suggestion section for items (one gender) missing from the user's wardrobe
if missing_items_one_gender:
    # Display message with suggested items that are not in the wardrobe but recommended for current weather
    st.write("Depending on your gender preference, you might consider purchasing the following clothes:")
    bullet_points = "\n".join(
        [f"- {item}" for item in missing_items_one_gender]
    )  # To list the missing items in bullet points
    st.markdown(bullet_points, unsafe_allow_html=True)

# Extra Space for better Mobile Display
st.header('')
st.header('')
