import streamlit as st
from fetch_data import fetch_github_data
from data_preprocess import preprocess_data

st.set_page_config(
    page_title="GitHub Activity Dashboard",
    page_icon=":octocat:",
    layout="wide"
)

st.title("GitHub Activity Dashboard")

