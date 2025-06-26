from collections import Counter
import pandas as pd
import pytz
from datetime import datetime

def preprocess_data(df):
    """
    Selects and renames relevant columns for display, drop null columns and manage type of column.
    """
    if df is None or df.empty:
        return pd.DataFrame()

    # Subsetting the columns
    df = df[['name','stargazers_count', 'forks_count', 'language', 'html_url', 'created_at', 'updated_at','year']]

    # Renaming columns for better readability
    df = df.rename(columns={
        'name': 'Repository Name',
        'stargazers_count': 'Stars',
        'forks_count': 'Forks',
        'language': 'Language',
        'html_url': 'Repository URL',
        'created_at': 'Created At',
        'updated_at': 'Updated At',
        'year': 'Year'
    })

    # Converting 'created_at' and 'updated_at' to datetime
    df['Created At'] = pd.to_datetime(df['Created At']).dt.tz_convert(pytz.utc)
    df['Updated At'] = pd.to_datetime(df['Updated At']).dt.tz_convert(pytz.utc)

    # Getting current date and making timezone aware
    today_date = pd.Timestamp(datetime.now(pytz.utc))

    df['Repo age days'] = (today_date - df['Created At']).dt.days
    df['Repo age years'] = df['Repo age days']/365

    # Star and Fork growth rates
    df['Star Growth Rate'] = df['Stars'] / df['Repo age years']
    df['Fork Growth Rate'] = df['Forks'] / df['Repo age years']

    # Calculating activity score
    df['Activity Score'] = df['Star Growth Rate'] * 0.7 + df['Fork Growth Rate'] * 0.3

    # Remove rows with null values
    df = df.dropna()

    return df

def repo_counts_per_language_per_year(df):
    '"Counts the number of repositories per language per year and returns a DataFrame."'
    if df is None or df.empty:
        return pd.DataFrame()
    
    # Grouping by language and year, then counting repositories
    df= df.groupby(['Language', 'Year']).size().reset_index(name='Repo Count')
    
    df = df.sort_values(by=['Year', 'Repo Count'], ascending=[True, False])

    return df

def preprocess_issues_pulls(response):
    df = pd.DataFrame({
                'Title': [pr['title'] for pr in response],
                'Created At': pd.to_datetime([pr['created_at'] for pr in response])
            })
    df['Count'] = 1
    df = df.sort_values('Created At')
    df['Cumulative Count'] = df['Count'].cumsum()

    return df

def count_commits_by_date(commits):
    dates = [commit['commit']['committer']['date'][:10] for commit in commits]
    date_counts = Counter(dates)
    df = pd.DataFrame(date_counts.items(), columns=['Date', 'Commits'])
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date')
    return df

def prepare_donut_data(user):
    repos = fetch_all_repos(user)
    data = []
    for repo in repos:
        name = repo['name']
        full_name = repo['full_name']
        count = get_commit_count(full_name)
        if count > 0:
            data.append({'Repository': name, 'Commits': count})
    return pd.DataFrame(data)

