import streamlit as st
import requests
import pandas as pd
from fetch_data import fetch_user_data

st.set_page_config(
    page_title="Your Activity Dashboard",
    page_icon=":bar_chart:",
)

st.markdown('# Profile & Repository Drilldown')

user_name = st.sidebar.text_input("Enter your GitHub username:", value="Rista10")

profile = fetch_user_data(user_name)

if profile is not None:
    st.subheader("👤 Profile Overview")
    st.write("######")

    col1, col2 = st.columns([1, 3])

    with col1:
        st.image(profile.loc[0, 'avatar_url'], width=100)

    with col2:
        st.write(f"**Username :** {profile.loc[0, 'login']}")
        
        c1, c2 = st.columns(2)

        with c1:
            with st.container(border=True):
                st.write(f"**Followers :** {profile.loc[0, 'followers']}")

        with c2:
            with st.container(border=True):
                st.write(f"**Following :** {profile.loc[0, 'following']}")

    st.write('#####')
    st.subheader("📊 Repository Overview")