import streamlit as st
from fetch_data import fetch_repository_contributions, fetch_repository_details, fetch_repository_issues_pulls, total_commits_over_time
from data_preprocess import preprocess_issues_pulls
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Repository Dashboard",
    page_icon=":octocat:",
    layout="wide"
)

# sidebar for repository name as input
# watchers, stars, forks : 3 cards
# show below 3 in a column
# top pr contrbutions - comparison between top user contributions
# open pr over time - area chart
# open issues over time - bar chart

repo_name = st.sidebar.text_input("Enter the repository name:", value="deepseek-ai/DeepSeek-R1")
st.title(f"{repo_name} Repository Dashboard")
st.write('#####')

repo_data = fetch_repository_details(repo_name)

if repo_data:
    # --- Top Metrics Cards ---
    st.markdown("### Repository Overview")
    col1, col2, col3 = st.columns(3)
    
    col1.metric(":star: Stars", repo_data['stargazers_count'])
    col2.metric(":fork_and_knife: Forks", repo_data['forks_count'])
    col3.metric(":eye: Watchers", repo_data['watchers_count'])

    st.write('#####')
    # Contributions, pr and issues sections
    col1,col2,col3= st.columns(3)

    with col1:
        st.subheader("Top Contributors")
        contributors = fetch_repository_contributions(repo_data['contributors_url'])
        if contributors:
            top_contributors = sorted(contributors, key=lambda x: x['contributions'], reverse=True)[:7]
            fig = px.bar(
            top_contributors, 
            x='login', 
            y='contributions', 
            labels={'login': 'Contributor', 'contributions': 'Number of Contributions'},
            color='contributions',
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No contributors data available.")

    with col2:
        st.subheader("Cumulative Open Pull Requests")
        open_pull_request = fetch_repository_issues_pulls(repo_name, type='pulls')
        if open_pull_request:
            open_prs = [pr for pr in open_pull_request if pr['state'] == 'open']
            # open_pr_count = len(open_prs)
            # st.write(f"Total Open Pull Requests: {open_pr_count}")

            df = preprocess_issues_pulls(open_prs)
            
            fig = px.area(
                df,
                x='Created At',
                y='Cumulative Count',
                # title='Cumulative Open Pull Requests Over Time',
                labels={'Created At': 'Date', 'Cumulative Count': 'Total Open PRs'}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No open pull requests available.")

    with col3:
        st.subheader("Open Issues Over Time")
        open_issues = fetch_repository_issues_pulls(repo_name, type='issues')
        if open_issues:
            open_issues = [issue for issue in open_issues if issue['state'] == 'open']
            df = preprocess_issues_pulls(open_issues)
            
            fig = px.area(
                df,
                x='Created At',
                y='Cumulative Count',
                # title='Open Issues Over Time',
                labels={'Created At': 'Date', 'Cumulative Count': 'Total Open Issues'}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No open issues available.")

# commits over time
commits_over_time = total_commits_over_time(repo_name)


st.write('#####')
st.subheader("Total Commits Over Time")
fig = px.line(commits_over_time, x="day", y="commits", 
                title=f"Commits Over Time for {repo_name}",
                labels={"day": "Date", "commits": "Number of Commits"})
st.plotly_chart(fig, use_container_width=True)

# correlation between languages
# correlation between language and job

