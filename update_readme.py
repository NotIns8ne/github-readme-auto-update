import os
import subprocess
from github import Github

# Load GitHub token from environment variable
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable is not set.")

# Initialize GitHub API client
g = Github(GITHUB_TOKEN)

# GitHub username and repository
GITHUB_USERNAME = "SyntaxSkater"
REPO_NAME = f"{GITHUB_USERNAME}/{GITHUB_USERNAME}"
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
            continue

        print(f"Analyzing repository: {repo.name}")
        languages = repo.get_languages()
        lang_string = ", ".join(languages.keys()) if languages else "No languages detected"

        repo_data.append({
            "name": repo.name,
            "description": repo.description or "No description available.",
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

def overwrite_remote_readme(content):
    """
    Overwrite the remote README.md on GitHub.
    """
    print("Overwriting README.md on GitHub...")
    repo = g.get_repo(REPO_NAME)
    try:
        # Get the current README file and update its content
        readme = repo.get_readme()
        repo.update_file(
            path=readme.path,
            message="Update README.md via script",
            content=content,
            sha=readme.sha
        )
        print("README.md updated successfully on GitHub.")
    except Exception as e:
        print(f"Error updating README.md on GitHub: {e}")

def main():
    """
    Main function to fetch GitHub activity, generate README content, and update the remote file.
    """
    try:
        repo_data = get_github_activity()
        new_readme_content = generate_readme_content(repo_data)
        overwrite_remote_readme(new_readme_content)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
