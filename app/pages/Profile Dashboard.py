import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from fetch_data import fetch_user_data, fetch_user_most_used_languages, fetch_commit_activity

st.set_page_config(
    page_title="Your Activity Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
)

st.markdown('# Profile & Repository Drilldown')

user_name = st.sidebar.text_input("Enter your GitHub username:", value="Rista10")
if not user_name:
    st.sidebar.warning("Please enter a GitHub username.")
    st.stop()

profile = fetch_user_data(user_name)

if profile is not None:
    st.subheader("👤 Profile Overview")
    st.write("######")

    # Show avatar image in full width of col1
    col1, col2, col3,col4 = st.columns(4)

    with col1:
        st.image(profile.loc[0, 'avatar_url'], width=100, caption="Avatar")
    
    with col2:
        st.markdown(f"### {profile.loc[0, 'name'] or profile.loc[0, 'login']}")
        st.markdown(f"🔗 [@{profile.loc[0, 'login']}](https://github.com/{profile.loc[0, 'login']})")

    with col3:
        st.metric("👥 Followers", profile.loc[0, 'followers'])

    with col4:
        st.metric("➡️ Following", profile.loc[0, 'following'])

st.write('#####')
st.subheader("📊 Repository Overview")

most_used_lang =fetch_user_most_used_languages(user_name)


col1, col2 = st.columns(2, gap="medium")

with col1:
    if most_used_lang is None:
        st.write("No data available for the most used languages.")
    
    df = pd.DataFrame(most_used_lang.items(), columns=['Language', 'Usage'])

    # sort value by usage in descending order
    top_languages= df.sort_values(by='Usage', ascending=False).head(6)

    fig = px.pie(
        names=top_languages['Language'],
        values=top_languages['Usage'],
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title="Most used programming languages in your repositories"
    )
    
    st.plotly_chart(fig, use_container_width=True)

activity_by_repo, monthly_commit_data = fetch_commit_activity(user_name)

with col2:
    if activity_by_repo:
        repo_df = pd.DataFrame({
            "Repository": list(activity_by_repo.keys()),
            "Commits": list(activity_by_repo.values())
        }).sort_values("Commits", ascending=False)

        top_repos = repo_df.head(10)

        fig = px.pie(top_repos, names="Repository", values="Commits", hole=0.4, title="Top 10 Repositories by Commit Count")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No repository activity found.")


# heatmap of daily contributions : weekday vs months
# commits over time: monthly commits- line chart
# commits by repository - donut chart


# Commits over time
st.subheader("📈 Monthly Commits Trend")


if monthly_commit_data:
    commit_df = pd.DataFrame({
        "Month": list(monthly_commit_data.keys()),
        "Commits": list(monthly_commit_data.values())
    }).sort_values("Month")

    fig = px.line(commit_df, x="Month", y="Commits", markers=True, title="Monthly Commits Over Time")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No commit data found.")

