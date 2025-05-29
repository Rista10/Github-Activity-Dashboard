import requests
import os
from dotenv import load_dotenv
import pandas as pd
import streamlit as st

load_dotenv()
GITHUB_PAT = os.getenv('PAT_TOKEN')

import requests
import pandas as pd
import time
import streamlit as st

@st.cache_data(show_spinner=True)
def fetch_github_data(start_year=None, end_year=None, top_n=100, github_token=None):
    """
    Fetch GitHub repositories over a range of years for a given language.

    Args:
        language (str): The programming language to filter by.
        start_year (int): Starting year of the range.
        end_year (int): Ending year of the range.
        top_n (int): Max number of repositories per year (max 100 per GitHub API page).
        github_token (str, optional): GitHub personal access token for authenticated requests.

    Returns:
        pd.DataFrame: Combined DataFrame with repository data.
    """

    base_url = "https://api.github.com/search/repositories"
    headers = {
    "Authorization":f"Bearer {GITHUB_PAT}",
    "Accept":"application/vnd.github.v3+json"}

    all_data = []

    for year in range(start_year, end_year + 1):
        query = f"stars:>0"

        query += f" created:{year}-01-01..{year}-12-31"

        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": min(top_n, 100)  
        }

        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            df_year = pd.json_normalize(data['items'])  
            df_year['year'] = year  
            all_data.append(df_year)
        else:
            print(f"Error: {response.status_code} - {response.text}")
            continue

        time.sleep(1)

    if all_data:
        df_all = pd.concat(all_data, ignore_index=True)
        return df_all
    else:
        return pd.DataFrame()

    
def fetch_user_data(username):
    """
    Fetches user data from GitHub API.
    
    Args:
        username (str): The GitHub username to fetch data for.
    
    Returns:
        dict: A dictionary containing user data.
    """
    
    url = f"https://api.github.com/users/{username}"
    headers = {
        "Authorization": f"token {GITHUB_PAT}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame([data])
        return df
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    
