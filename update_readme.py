import os
import subprocess
from github import Github
from datetime import datetime

# Load GitHub token from environment variable
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable is not set.")

# Initialize GitHub API client
g = Github(GITHUB_TOKEN)

# GitHub username and repository
GITHUB_USERNAME = "SyntaxSkater"
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

def fetch_remote_readme():
    """
    Fetch the README.md content from the GitHub profile repository.
    """
    print("Fetching the current README.md from GitHub...")
    repo = g.get_repo(REPO_NAME)
    try:
        readme_content = repo.get_readme().decoded_content.decode("utf-8")
        print("Successfully fetched remote README.md.")
        return readme_content
    except Exception as e:
        print(f"Error fetching remote README.md: {e}")
        return None

def update_readme_locally(content):
    """
    Update the README file locally.
    """
    print(f"Updating {README_PATH} locally...")
    with open(README_PATH, "w", encoding="utf-8") as readme_file:
        readme_file.write(content)
    print(f"{README_PATH} updated locally.")

def force_commit_and_push():
    """
    Force stage, commit, and push the README file to GitHub.
    """
    print("Forcing changes to be staged, committed, and pushed...")
    try:
        # Explicitly add README.md
        subprocess.run(["git", "add", README_PATH], check=True)

        # Check if README.md is staged
        staged_files = subprocess.run(["git", "diff", "--cached", "--name-only"], check=True, stdout=subprocess.PIPE, text=True).stdout.strip()
        if README_PATH not in staged_files:
            print(f"{README_PATH} is not staged. Forcing staging.")
            subprocess.run(["git", "add", README_PATH], check=True)

        # Commit the changes
        commit_message = f"Update README.md - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Push the changes
        subprocess.run(["git", "push"], check=True)

        print("Changes pushed to GitHub successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during Git operation: {e}")

def main():
    """
    Main function to update README and push changes.
    """
    try:
        repo_data = get_github_activity()
        new_readme_content = generate_readme_content(repo_data)

        # Fetch the current remote README.md content
        remote_readme_content = fetch_remote_readme()

        # Compare local and remote README.md
        if remote_readme_content is None or remote_readme_content.strip() != new_readme_content.strip():
            print("Local README.md does not match remote README.md. Updating...")
            update_readme_locally(new_readme_content)
            force_commit_and_push()
        else:
            print("Local README.md matches remote README.md. No updates needed.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
