import streamlit as st
from streamlit_calendar import calendar
import datetime
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="JACKSON AI",
    page_icon="🧠",
    layout="centered"
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .stTextInput input, .stSelectbox select, .stSlider div {
        border-radius: 5px;
        border: 1px solid #ccc;
    }
    .stHeader {
        color: #4CAF50;
        font-size: 36px;
        font-weight: bold;
    }
    .stBanner {
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-size: 20px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Session state to store user data
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
if "mood_data" not in st.session_state:
    st.session_state.mood_data = {}
if "stress_data" not in st.session_state:
    st.session_state.stress_data = {}

# Login Page
def login_page():
    st.markdown('<p class="stHeader">JACKSON AI</p>', unsafe_allow_html=True)
    st.write("Please log in to continue.")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "user" and password == "password":  # Simple hardcoded login
            st.session_state.logged_in = True
            st.session_state.registration_banner = True
            st.success("Logged in successfully! 🎉")
        else:
            st.error("Invalid username or password.")

# Role Selection Page
def role_selection_page():
    st.markdown('<p class="stHeader">JACKSON AI</p>', unsafe_allow_html=True)
    st.title("Select Your Role")
    role = st.radio("Are you a:", ("Student", "Worker"))

    if st.button("Continue"):
        st.session_state.role = role
        st.success(f"Welcome, {role}! 🎉")
        st.experimental_rerun()  # Refresh the app to show the next page

# Calendar Page
def calendar_page():
    st.markdown('<p class="stHeader">JACKSON AI</p>', unsafe_allow_html=True)
    st.title(f"📅 {st.session_state.role} Calendar")

    # Display calendar
    today = datetime.date.today()
    selected_date = st.date_input("Select a date", today)

    # Mood and Stress Input
    st.subheader("How are you feeling?")
    mood = st.selectbox(
        "Select your mood:",
        ["😊 Happy", "😐 Neutral", "😔 Sad", "😡 Angry", "😰 Anxious"]
    )
    stress_level = st.slider("Rate your stress level (1-10):", min_value=1, max_value=10, value=5)

    if st.button("Log Entry"):
        st.session_state.mood_data[selected_date] = mood
        st.session_state.stress_data[selected_date] = stress_level
        st.success("Entry logged successfully! 🎉")

    # Display logged data
    st.subheader("Your Logged Data")
    if st.session_state.mood_data:
        for date, mood in st.session_state.mood_data.items():
            st.write(f"📅 {date}: {mood}, Stress Level: {st.session_state.stress_data[date]}")
    else:
        st.write("No data logged yet.")

# Dashboard Page
def dashboard_page():
    st.markdown('<p class="stHeader">JACKSON AI</p>', unsafe_allow_html=True)
    st.title("📊 Dashboard")
    st.write(f"Hello, {st.session_state.role}! Here's your mental health summary.")

    if st.session_state.mood_data:
        # Calculate average stress level
        avg_stress = sum(st.session_state.stress_data.values()) / len(st.session_state.stress_data)
        st.write(f"📈 Average Stress Level: {avg_stress:.1f}/10")

        # Mood distribution chart
        mood_counts = {}
        for mood in st.session_state.mood_data.values():
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
        st.write("📊 Mood Distribution:")
        fig = px.pie(values=list(mood_counts.values()), names=list(mood_counts.keys()), title="Mood Distribution")
        st.plotly_chart(fig)
    else:
        st.write("No data available yet.")

# Main App Logic
def main():
    if not st.session_state.logged_in:
        login_page()
    elif st.session_state.logged_in and st.session_state.role is None:
        role_selection_page()
    else:
        # Display registration banner
        if hasattr(st.session_state, "registration_banner") and st.session_state.registration_banner:
            st.markdown('<div class="stBanner">Thank you for registering!</div>', unsafe_allow_html=True)
            st.session_state.registration_banner = False

        # Navigation sidebar
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ("Calendar", "Dashboard"))

        if page == "Calendar":
            calendar_page()
        elif page == "Dashboard":
            dashboard_page()

# Run the app
if __name__ == "__main__":
    main()