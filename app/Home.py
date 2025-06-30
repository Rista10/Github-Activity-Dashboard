import streamlit as st
from PIL import Image
import os

# Page configuration
st.set_page_config(
    page_title="GitHub Activity Dashboard",
    page_icon=":bar_chart:",
    layout="centered"
)

# Title and logo
st.title("📊 GitHub Activity Dashboard")
st.markdown("Welcome to the interactive GitHub Activity Dashboard built with **Streamlit**.")

script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.normpath(os.path.join(script_dir, "../assets/background-image.webp"))
logo = Image.open(image_path)
st.image(logo)

# Project overview
st.markdown("""
This dashboard allows you to explore real-time GitHub data, visualized through three interactive modules:

1. **Profile Dashboard**  
   View your user profile overview, most used programming languages, and their activities.

2. **Language Trends Dashboard**  
   Analyze language usage patterns over time, repository popularity, and collaboration levels.

3. **Repository Dashboard**  
   Dive deep into any repository to explore stars, forks, top contributors, and activity insights.

---  
""")

# Instructions
st.subheader("🔍 How to Use")
st.markdown("""
- Use the sidebar to navigate between dashboards.
- Visualizations will update based on your input.

All data is retrieved in real-time using the **GitHub REST API** and visualized using **Plotly Express**.
""")

# Footer
st.markdown("---")
st.markdown("Made with using [Streamlit](https://streamlit.io/) | Powered by [GitHub API](https://docs.github.com/en/rest?apiVersion=2022-11-28)")

