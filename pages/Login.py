import streamlit as st

# https://arnaudmiribel.github.io/streamlit-extras/extras/switch_page_button/
from streamlit_extras.switch_page_button import switch_page

# load up the db
db = st.session_state.get("db", None)
if db is None:
    switch_page("Main")
    
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

st.title("Login to NimbusWardrobe")

email = st.text_input("Email:")
password = st.text_input("Password:", type="password")

# Check if the "Login" button has been clicked
if st.button("Login"):
    user_id = db.authenticate_user(email, password)
    # If the "Login" button is clicked, it calls the authenticate_user function
    # with the provided useremail and password
    if user_id is not None and isinstance(user_id, int):
        # Save the user_id in session_state
        st.session_state["current_user_id"] = user_id
        st.success("Login successful!")
        switch_page("Main")
    else:
        st.error("Authentication failed. Please check your email and password.")

# Should the user not have an account yet, leading them to the "Register" page.
if st.button("No account? Create one!"):
    switch_page("Register")


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
