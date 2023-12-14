# Import of the libraries needed for the web application
# Reference: Course Content
import bcrypt
import pandas as pd
import sqlite3
import streamlit as st

from streamlit_extras.switch_page_button import switch_page

# API key for accessing OpenWeatherMap
# Reference: https://openweathermap.org/guide
API_KEY_OPEN_WEATHER = "fd52fa375b7a291780785bd3a1b46caa"

# DB filepath
DB_FILE_PATH = "nimbus_wardrobe.db"

# Definition of categories and corresponding items for wardrobe management,
# allowing users to choose from predefined categories and items
CATEGORIES = {
    "Outerwear": [
        "Winter Jacket/Coat",
        "Wool Coat",
        "Parka",
        "Trench Coat",
        "Lightweight Down Jacket",
        "Softshell Jacket",
        "Leather Jacket",
        "Denim Jacket",
        "Raincoat",
        "Windbreaker",
        "Blazer",
    ],
    "Topwear": [
        "Long-Sleeve Shirt",
        "T-Shirt",
        "Short-Sleeve Blouse",
        "Long-Sleeve Blouse",
        "Long-Sleeve Dress",
        "Short-Sleeve Dress",
        "Tank Top",
    ],
    "Layering": ["Heavy Sweater", "Fleece/Thermal Layer", "Cardigan", "Hoodie", "Lightweight Sweater"],
    "Bottomwear": ["Snow Pants", "Pants", "Jeans", "Capri Pants", "Shorts", "Skirt"],
    "Footwear": [
        "Insulated Winter Boots",
        "Classic Boots",
        "Ankle Boots",
        "Sneakers",
        "Loafers",
        "Sandals",
        "Rubber Rain Boots",
    ],
    "Accessories": [
        "Sunglasses",
        "Umbrella",
        "Belt",
        "Warm Scarf",
        "Light Scarf",
        "Beanie",
        "Cap",
        "Insulated Winter Gloves/Mittens",
        "Standard Gloves/Mittens",
        "Thermal Socks",
        "Socks",
        "Thermal Leggings/Tights",
    ],
}


# DataBase class definition
class DataBase:
    def __init__(self):
        """
        Initialize the new database if the file does not exit
        'user' table
            - id: allocated id for the user
            - email: email registered for the user
            - password: hashed password for the user
        'wardrobe' table
            - user_id: the user's id that the item belongs to
            - category: the item category
            - sub_category: the item sub category
            - name: the custome name for the item that the user provides
        """
        self.con = sqlite3.connect(DB_FILE_PATH)
        with self.con as DB:
            DB.execute(
                "CREATE TABLE IF NOT EXISTS user "
                + "(id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE, password TEXT);"
            )
            DB.execute(
                "CREATE TABLE IF NOT EXISTS wardrobe "
                + "(user_id INTEGER, category TEXT, sub_category TEXT, name TEXT);"
            )

    def add_user(self, email, password):
        """
        Add a new user

        Params:
        - email: str
        - password: str

        Return:
        - the new user id (int)
        """
        # hashing passwords with bcrypt, salt value added for additional security,
        # the bcrypt.hashpw returns a bytes object that's why it's transformed in string
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        with self.con as DB:
            user_id = DB.execute(
                "INSERT INTO user (email, password) VALUES (?, ?);",
                (email, hashed_password.decode("utf-8")),
            ).lastrowid
            return user_id

    def add_wardrobe_item(self, user_id, category, sub_category, name):
        """
        Add a new item to the user's wardrobe

        Params:
        - user_id: the id for the user (int)
        - category: str
        - sub_category: str
        - name: str

        Return:
        - the new wardrobe item id (int)
        """
        with self.con as DB:
            item_id = DB.execute(
                "INSERT INTO wardrobe (user_id, category, sub_category, name) VALUES (?, ?, ?, ?);",
                (user_id, category, sub_category, name),
            ).lastrowid
            return item_id

    def authenticate_user(self, email, password):
        """
        Authenticate the user by email and password

        Params:
            - email: str
            - password: str

        Return: boolean
        """
        stored_password = None
        with self.con as DB:
            c = DB.cursor()
            # This SQL query is executed to select the hashed password from the user table
            # where the provided useremail matches
            c.execute("SELECT password FROM user WHERE email = ?", (email,))
            res = c.fetchone()
            if len(res) == 1:
                stored_password = res[0]
            else:
                return False

        # Check if stored_password is not None (i.e., a user with the provided useremail exists)
        # and then it uses bcrypt.checkpw to compare the hashed password stored in the database
        # with the hashed version of the provided password
        if stored_password and bcrypt.checkpw(password.encode("utf-8"), stored_password.encode("utf-8")):
            return True
        return False

    def check_wardrobe_for_items(self, user_id, recommended_items):
        """
        Initialize lists to keep track of present and missing items in the wardrobe

        Params:
            - user_id:
            - recommended_items: ?

        Return:
            - present_items: ?
            - missing_items_both_genders: ?
            - missing_items_one_gender: ?
            - detailed_present_items: ?
        """
        # list about missing user items for one gender
        one_gender_list = [
            "Long-Sleeve Shirt",
            "Long-Sleeve Blouse",
            "Long-Sleeve Dress",
            "Blazer",
            "Short-Sleeve Blouse",
            "Short-Sleeve Dress",
            "Skirt",
        ]
        # To create list about present user items
        present_items = []
        # To create list about missing user items for both genders
        missing_items_both_genders = []
        # To create list about missing user items for one gender
        missing_items_one_gender = []
        # To create list to collect detailed information about present user items
        detailed_present_items_rows = []

        # To retrieve the current items in the user's wardrobe from the database
        wardrobe_items = self.get_wardrobe_items(user_id)

        # To iterate over each category and its items in the recommended items
        for category, items in recommended_items.items():
            for item in items:  # To check if the current item is in the user's wardrobe
                if item in wardrobe_items["sub_category"].values:
                    present_items.append(item)  # If present, add to the list of present items
                    detailed_present_items_rows.append(
                        wardrobe_items[wardrobe_items["sub_category"] == item]
                    )  # To collect detailed information about this item
                elif item not in one_gender_list:
                    missing_items_both_genders.append(
                        item
                    )  # If not present, to add to the list of missing items for both genders

                elif item in one_gender_list:
                    missing_items_one_gender.append(
                        item
                    )  # If not present, to add to the list of missing items for one gender

        # To create a DataFrame from the collected rows of present items
        # If there are no present items, to create an empty DataFrame
        print(detailed_present_items_rows)
        detailed_present_items = (
            pd.concat(detailed_present_items_rows, ignore_index=True) if detailed_present_items_rows else pd.DataFrame()
        )

        # To return the lists of present and missing items, and the DataFrame of detailed present items
        return present_items, missing_items_both_genders, missing_items_one_gender, detailed_present_items

    def get_wardrobe_items(self, user_id):
        """
        Retrieve the current wardrobe items for a specific user from the database
        to execute an SQL query to select all records from the user's wardrobe table
        with the query fetching all rows and columns from the specified table.

        Params:
        - user_id: int

        Return:
        - df: pd.DataFrame contains the wardrobe items
        """
        with self.con as DB:
            df = pd.read_sql(f"SELECT category, sub_category, name FROM wardrobe WHERE user_id = {user_id};", DB)

            # Print the column names of the DataFrame for debugging
            # or informational purposes to help in understanding the structure of
            # the retrieved data
            print("DataFrame Columns:", df.columns)  # Add this line to print the column names

            # To return the DataFrame containing the user's wardrobe items
            return df

    def remove_wardrobe_item(self, user_id, name):
        """
        Remove a item from the user's wardrobe by id

        Params:
        - user_id: the user id that the item to be removed belongs to (int)
        - name: the wardrobe item name to be removed (str)

        Return:
        - None
        """
        with self.con as DB:
            DB.execute(f"DELETE FROM wardrobe WHERE user_id = {user_id} AND name = '{name}'")


# Main Page - Function to display the main page of the app
# Reference:
# - https://docs.streamlit.io/library/api-reference/text/st.markdown
# - https://docs.streamlit.io/library/api-reference/text/st.title
# - https://docs.streamlit.io/library/api-reference/widgets/st.text_input;
def main_page():
    # Access the stored user_id from session_state
    current_user_id = st.session_state.get("current_user_id", None)
    if current_user_id is None:
        st.write("Please login first.")
        switch_page("Login")

    # To set a background image for the app
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://wallpaper.dog/large/20426356.jpg");
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Title of the main page
    st.title("Welcome to NimbusWardrobe")

    # Introductory text explaining the purpose of the app
    st.write(
        "In order to provide you with an outfit recommendation for the current weather, "
        + "we need to know a little about you and your personal wardrobe."
    )

    # Operations to perform if the user has entered an email
    # Reference:
    # - https://docs.streamlit.io/library/api-reference/text/st.header
    # - https://docs.streamlit.io/library/api-reference/write-magic/st.write
    # - https://docs.streamlit.io/library/api-reference/text/st.subheader
    # - https://docs.streamlit.io/library/api-reference/data/st.dataframe

    # Fetch the current wardrobe items from the database
    df_wardrobe = db.get_wardrobe_items(current_user_id)

    # To display the user's current wardrobe if it's not empty
    if not df_wardrobe.empty:
        print("DataFrame Columns:", df_wardrobe.columns)
        st.header("Your Current Wardrobe")
        st.write("It appears that you have the following wardrobe items registered on NimbusWardrobe:")

        # To loop through categories and display each category's items in the wardrobe
        for category in CATEGORIES.keys():
            st.subheader(f"{category} Items")
            # Ensure the column name used here matches exactly with what's printed above
            df_category = df_wardrobe[df_wardrobe["category"] == category]
            if not df_category.empty:
                st.dataframe(df_category,hide_index=True)
            else:
                st.write(f"No items found in the {category} category.")

    # Section for managing the user's wardrobe
    # Reference:
    # - https://docs.streamlit.io/library/api-reference/widgets/st.selectbox
    # - https://docs.streamlit.io/library/api-reference/widgets/st.text_input
    # - https://docs.streamlit.io/library/advanced-features/button-behavior-and-examples
    # - https://docs.streamlit.io/library/api-reference/text/st.header
    st.header("Manage Your Wardrobe")
    st.write("Please enter all your wardrobe items, if you haven't done so already:")

    # Drop-down menu for selecting a category
    category = st.selectbox("Select the category of your wardrobe item:", list(CATEGORIES.keys()))
    # Drop-down menu for selecting an item within the chosen category
    sub_category = st.selectbox("Select the sub category:", CATEGORIES[category])
    # Text input for giving a custom name to the item
    name = st.text_input("Please name this item in your wardrobe:")
    # Button to submit the new item to the wardrobe
    if st.button("Submit New Item"):
        # Add the new item to the user's wardrobe in the database
        item_id = db.add_wardrobe_item(current_user_id, category, sub_category, name)
        # Display a confirmation message upon successful addition
        st.success("Item added to your wardrobe!")
        # Refresh the wardrobe items to include the newly added item
        df_wardrobe = db.get_wardrobe_items(current_user_id)

    if current_user_id:
        # Section for removing items from the user's wardrobe
        st.header("Remove Items from Your Wardrobe")
        st.write("Please remove any items that no longer belong in your wardrobe:")
        df_wardrobe = db.get_wardrobe_items(current_user_id)
        if not df_wardrobe.empty:
            # Add a select box for users to choose which item to delete
            item_to_remove = st.selectbox("Select an item to remove:", df_wardrobe["name"])
            if st.button("Remove Selected Item"):
                db.remove_wardrobe_item(current_user_id, item_to_remove)
                st.success("Item removed from your wardrobe!")
                # Refresh the wardrobe items
                df_wardrobe = db.get_wardrobe_items(current_user_id)
        else:
            st.write("Your wardrobe is currently empty.")

    # Section for user to input weather and get clothing recommendation
    st.header("Check Local Weather for Clothing Advice")
    # Text input for entering the city name
    city_input = st.text_input("Enter the name of your city to get the current weather:", key="city_input")

    # Button to get clothing recommendations based on the entered city
    if st.button("Get Recommendations"):
        # Process the city input and get recommendations
        st.session_state["city_name"] = city_input
        switch_page("Result")

    # Extra space for mobile display
    st.header('')
    st.header('')

# Background box
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://wallpaper.dog/large/20426356.jpg");
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

# App execution when this script is run directly
# Reference:
# - https://docs.streamlit.io/library/api-reference/layout/st.sidebar
# - https://discuss.streamlit.io/t/streamlit-is-repeatedly-running-a-loop-when-entering-details/45583
if __name__ == "__main__":
    # Initialize the database as a global object
    db = DataBase()
    st.session_state["db"] = db
    main_page()
