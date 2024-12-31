import os
import requests
from github import Github
from datetime import datetime

# Load GitHub token from environment variable
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable is not set.")

# Initialize GitHub API client
g = Github(GITHUB_TOKEN)

# GitHub username
GITHUB_USERNAME = "SyntaxSkater"

# Repository name
REPO_NAME = f"{GITHUB_USERNAME}/{GITHUB_USERNAME}"

# README file path
README_PATH = "README.md"


def get_github_activity():
    """
    Fetch recent public repositories and their details.
    """
    print("Fetching recent repositories...")
    user = g.get_user(GITHUB_USERNAME)
    repos = user.get_repos()

    repo_data = []
    for repo in repos:
        if repo.private:
            continue  # Skip private repos

        print(f"Analyzing repository: {repo.name}")
        languages = repo.get_languages()
        lang_string = ", ".join(languages.keys()) if languages else "No languages detected"

        repo_data.append({
            "name": repo.name,
            "description": repo.description or "No description provided.",
            "languages": lang_string,
            "last_updated": repo.updated_at.strftime("%Y-%m-%d"),
        })

    print(f"Found {len(repo_data)} repositories.")
    return repo_data


def generate_readme_content(repo_data):
    """
    Generate the content for the README file.
    """
    print("Generating README content...")
    content = f"# Hi, I'm {GITHUB_USERNAME} 👋\n\n"
    content += "Welcome to my GitHub profile! Here's a snapshot of my public repositories:\n\n"

    for repo in repo_data:
        content += f"## {repo['name']}\n"
        content += f"**Description:** {repo['description']}\n\n"
        content += f"**Languages:** {repo['languages']}\n\n"
        content += f"**Last Updated:** {repo['last_updated']}\n\n"
        content += "---\n\n"

    print("README content generated successfully.")
    return content


def update_readme():
    """
    Update the README file with the latest content.
    """
    repo_data = get_github_activity()
    new_content = generate_readme_content(repo_data)

    print(f"Updating {README_PATH}...")
    with open(README_PATH, "w", encoding="utf-8") as readme_file:
        readme_file.write(new_content)
    print(f"{README_PATH} updated successfully.")


if __name__ == "__main__":
    update_readme()
