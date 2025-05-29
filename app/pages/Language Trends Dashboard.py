import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px
import matplotlib.pyplot as plt
from fetch_data import fetch_github_data
from data_preprocess import preprocess_data,repo_counts_per_language_per_year

st.set_page_config(
    page_title="Language Trends Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
)

st.title("Language and Project Growth Trends")
st.markdown("This dashboard provides insights into the growth trends of programming languages and projects on GitHub. You can filter by language and year to see how different languages have evolved over time.")

language = st.sidebar.multiselect(
    "Select Programming Languages",
    options=["Python", "JavaScript", "Java", "C#", "C++", "Ruby", "PHP", "Go", "Swift", "TypeScript"],
    default=["Python"]
)

year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=2008,
    max_value=2025,
    value=(2008, 2025),
    step=1
)

uploaded_file = st.sidebar.file_uploader("Upload a CSV file with repository data", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    # Fetching data from GitHub API
    df = fetch_github_data(start_year=year_range[0], end_year=year_range[1])
    df = df[df['language'].isin(language)]

# Preprocessed dataframe
df_processed = preprocess_data(df)

st.expander("View Raw Data", expanded=False).write(df_processed)

# Grouping repo per year per language 
df_language_year = repo_counts_per_language_per_year(df_processed)


def display_repolanguages_per_year(df,start_year, end_year, frame_dir="frames"):
    st.subheader(f"GitHub Project Per Language Growth: {start_year} to {end_year}")

    year = st.slider("Select Year", start_year, end_year, start_year)

    yearly_data = df[df['Year'] == year].sort_values(by='Repo Count', ascending=True)
    
    fig, ax = plt.subplots(figsize=(16, 10), facecolor='none')
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')

    ax.barh(yearly_data['Language'], yearly_data['Repo Count'], color='skyblue')
    ax.set_title(f'GitHub Repo Growth - {year}', fontsize=20, color='white', pad=50)
    ax.set_xlabel('Repository Count',color='white', fontsize=16, labelpad=20)
    ax.set_ylabel('Language', color='white',fontsize=16,labelpad=20)

    ax.tick_params(colors='white')

    for spine in ax.spines.values():
        spine.set_edgecolor('white')

    st.pyplot(plt)

def popularity_vs_collaboration(df):
    st.subheader("Popularity vs Collaboration of each Repository")

    df = df[['Repository Name','Stars','Forks','Language']]

    fig,ax = plt.subplots(figsize=(16, 10), facecolor='none')
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')

    fig = px.scatter(df, x='Stars', y='Forks', color='Language',
                   hover_name='Repository Name',title='Popularity vs Collaboration',
                   labels={'Stars': 'Stars', 'Forks': 'Forks'},
                   color_discrete_sequence=px.colors.qualitative.Plotly)

    fig.update_traces(marker=dict(size=10, line=dict(width=2, color='DarkSlateGrey')), selector=dict(mode='markers'))
    st.plotly_chart(fig, use_container_width=True)

def language_trends_over_years(df):
    st.subheader("Language Trends Over the Years")
    
    df = df[['Year', 'Language', 'Star Growth Rate']].groupby(['Year', 'Language'], as_index=False).agg({'Star Growth Rate': 'sum'})

    fig = px.line(df, x='Year', y='Star Growth Rate', color='Language',
                  title='Language Trends Over the Years',
                  markers=True)

    fig.update_layout(legend_title_text='Programming Language')
    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2,gap="large")

with col1:
    display_repolanguages_per_year(df_language_year, year_range[0], year_range[1])

with col2:
    popularity_vs_collaboration(df_processed)
    
language_trends_over_years(df_processed)