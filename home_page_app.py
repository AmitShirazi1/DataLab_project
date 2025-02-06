import streamlit as st
import sys
import os

# Set page title with icon
st.set_page_config(page_title="Job interview Simulator", page_icon="📋✅", layout="wide")

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importing the 2 apps for the 2 simulations
import personality_test_app 
import job_interview_simulator_app

# Custom CSS
st.markdown("""
<style>
    /* Global Styling */
    :root {
        --primary-color: #2c3e50;      /* Deep navy blue */
        --secondary-color: #3498db;    /* Bright blue */
        --accent-color: #2ecc71;       /* Soft green */
        --background-color: #f4f6f8;   /* Light gray-blue */
        --text-color: #2c3e50;         /* Dark gray */
    }

    /* Base App Styling */
    .stApp {
        background-color: var(--background-color);
        font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
    }

    /* Title Styling */
    .stTitle {
        color: var(--primary-color);
        font-weight: 700;
        text-align: center;
        margin-bottom: 30px;
    }

    /* Button Styling */
    .stButton > button {
        background-color: var(--secondary-color);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .stButton > button:hover {
        background-color: var(--primary-color);
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }

    /* Card-like Containers */
    .stContainer {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }

    .stContainer:hover {
        transform: scale(1.02);
        box-shadow: 0 12px 25px rgba(0,0,0,0.12);
    }

    /* Radio Button Styling */
    .stRadio > div {
        background-color: white;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Title
    st.markdown("""
    <h1 style='text-align: center; 
               background: linear-gradient(to right, #2c3e50, #3498db);
               -webkit-background-clip: text;
               -webkit-text-fill-color: transparent;
               font-weight: 700;
               margin-bottom: 30px;'>
    Job interview Simulator
    </h1>
    """, unsafe_allow_html=True)

    # Subheader
    st.markdown("""
    <p style='text-align: center; 
              color: #7f8c8d; 
              font-size: 18px; 
              margin-bottom: 40px;'>
    Unlock Your Professional Potential through Advanced Assessments
    </p>
    """, unsafe_allow_html=True)

    # Create columns for side-by-side buttons with more space
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="stContainer" style="text-align: center; padding: 30px;">
            <h3 style="color: #2c3e50;">Personality Assessment</h3>
            <p style="color: #7f8c8d;">Discover your unique professional traits</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Start Personality Test 🧩", use_container_width=True):
            st.session_state.page = "personality"

    with col2:
        st.markdown("""
        <div class="stContainer" style="text-align: center; padding: 30px;">
            <h3 style="color: #2c3e50;">Interview Simulator</h3>
            <p style="color: #7f8c8d;">Prepare and practice for your dream job</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Launch Interview Simulator 🤝", use_container_width=True):
            st.session_state.page = "interview"
    
    # Render the selected page
    if hasattr(st.session_state, 'page'):
        if st.session_state.page == "personality":
            personality_test_app.main()
        elif st.session_state.page == "interview":
            job_interview_simulator_app.main()

if __name__ == "__main__":
    main()