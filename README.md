# GitHub Activity Dashboard

An interactive dashboard built with **Streamlit** to visualize real-time GitHub data, including user profiles, repository statistics, language trends, and contribution activity.

## Features

- **Profile Dashboard**: View GitHub user profiles, most used programming languages, and activity breakdowns.
- **Language Trends Dashboard**: Analyze programming language usage and repository growth over time.
- **Repository Dashboard**: Explore repository-level stats, top contributors, open issues, pull requests, and commit history.
- **Real-time Data**: Fetches live data from the GitHub REST API.
- **Interactive Visualizations**: Uses Plotly Express and Seaborn for dynamic charts.

## Setup

1. **Clone the repository**  
   ```sh
   git clone <your-repo-url>
   cd github-activity-dashboard
   ```

2. **Install dependencies**  
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up environment variables**  
   - Create a `.env` file in the root directory.
   - Add your GitHub Personal Access Token:
     ```
     PAT_TOKEN=your_github_pat_here
     ```

4. **Run the dashboard**  
   ```sh
   streamlit run app/Home.py
   ```

## Usage

- Use the sidebar to navigate between dashboards.
- Enter your GitHub username or repository name as prompted.
- Visualizations will update based on your input and selections.

## Notes

- The dashboard uses the GitHub API, which may be subject to rate limits.
- For best results, use a valid GitHub Personal Access Token with appropriate permissions.
