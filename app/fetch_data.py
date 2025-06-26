import requests
import os
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
from collections import defaultdict
import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup

load_dotenv()
GITHUB_PAT = os.getenv('PAT_TOKEN')


# Fetch GitHub repositories over a range of years for a given language
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

# Fetch user details 
@st.cache_data(show_spinner=True)   
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

# Fetch data about user most used programming language
@st.cache_data(show_spinner=True)
def fetch_user_most_used_languages(username):
    """
    Fetches the most used programming languages by a GitHub user.
    
    Args:
        username (str): The GitHub username.
    
    Returns:
        dict: A dictionary with languages as keys and total bytes of code as values.
    """

    url = f"https://api.github.com/users/{username}/repos"
    headers = {
        "Authorization": f"token {GITHUB_PAT}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        repos_data = response.json()

        language_totals = defaultdict(int)

        for repo in repos_data:
            languages_url = repo.get('languages_url')
            if languages_url:
                lang_response = requests.get(languages_url, headers=headers)
                if lang_response.status_code == 200:
                    languages_data = lang_response.json()
                    for lang, bytes_count in languages_data.items():
                        language_totals[lang] += bytes_count
                else:
                    print(f"Failed to fetch languages for {repo.get('name')}: {lang_response.status_code}")
        
        return dict(language_totals)
    else:
        print(f"Error fetching repos for user {username}: {response.status_code} - {response.text}")
        return None
    
# Single repository details
@st.cache_data(show_spinner=True)
def fetch_repository_details(repo_name):
    """
    Fetches details of a specific GitHub repository.
    
    Args:
        repo_name (str): The full name of the repository (e.g., "owner/repo").
    
    Returns:
        dict: A dictionary containing repository details.
    """
    
    url = f"https://api.github.com/repos/{repo_name}"
    headers = {
        "Authorization": f"token {GITHUB_PAT}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    
# Fetch repository contributions
@st.cache_data(show_spinner=True)
def fetch_repository_contributions(repo_contributors_url):
    headers = {
        "Authorization": f"token {GITHUB_PAT}"
    }
    response = requests.get(repo_contributors_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        contributions = []
        for contributor in data:
            contributions.append({
                "login": contributor.get("login"),
                "contributions": contributor.get("contributions"),
            })
        return contributions
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    
# Fetch repository issues and pull requests\
@st.cache_data(show_spinner=True)
def fetch_repository_issues_pulls(repo_name, type='issues'):
    """
    Fetches issues or pull requests for a specific GitHub repository.
    
    Args:
        repo_name (str): The full name of the repository (e.g., "owner/repo").
        issue_type (str): 'issues' or 'pulls' to specify the type of data to fetch.
    
    Returns:
        list: A list of issues or pull requests.
    """
    
    url = f"https://api.github.com/repos/{repo_name}/{type}"
    headers = {
        "Authorization": f"token {GITHUB_PAT}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    
@st.cache_data(show_spinner=True)
def total_commits_over_time(repo_name):
    url = f"https://api.github.com/repos/{repo_name}/commits"
    headers={
        "Authorization": f"token {GITHUB_PAT}"
    }
    response = requests.get(url,headers=headers)

    if response.status_code == 200:
        data = response.json()

        dates = [item["commit"]["author"]["date"] for item in data if "commit" in item]
        df = pd.DataFrame({"date": pd.to_datetime(dates)})
        df["day"] = df["date"].dt.date

        commit_counts = df.groupby("day").size().reset_index(name="commits")
        return commit_counts
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    

@st.cache_data(show_spinner=True)
def fetch_commit_activity(username):
    # Get repos
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100&type=owner"
    headers = {
        "Authorization": f"token {GITHUB_PAT}"
    }
    
    repos = requests.get(repos_url,headers=headers).json()

    activity_by_repo = {}
    monthly_commit_data = defaultdict(int)

    for repo in repos:
        repo_name = repo['name']
        commits_url = f"https://api.github.com/repos/{username}/{repo_name}/commits?per_page=100"
        commits = requests.get(commits_url,headers=headers).json()
        
        if isinstance(commits, list):
            activity_by_repo[repo_name] = len(commits)
            for commit in commits:
                if commit.get('commit'):
                    date = commit['commit']['author']['date']
                    month = pd.to_datetime(date).strftime('%Y-%m')
                    monthly_commit_data[month] += 1

    return activity_by_repo, dict(monthly_commit_data)