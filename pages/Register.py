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


st.title("Register to NimbusWardrobe")

new_email = st.text_input("New Email:")
new_password = st.text_input("New Password:", type="password")
confirm_password = st.text_input("Confirm Password:", type="password")

if st.button("Register"):
    user_id = db.add_user(new_email, new_password)
    if new_password == confirm_password and isinstance(user_id, int):
        st.session_state["current_user_id"] = user_id
        st.success(f"Registration successful! (user_id: {user_id}) You can now log in as {new_email}.")
        switch_page("Main")
    else:
        st.error("Passwords do not match. Please try again.")

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
