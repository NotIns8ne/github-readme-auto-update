# GitHub README Auto Update

Automatically updates your GitHub profile `README.md` with your latest repositories, activities, and details. This tool fetches data from your GitHub account using the GitHub API and synchronizes it to your profile.

---

## How It Works

- Fetches your public repositories, including their names, descriptions, languages, and last updated dates.
- Compares the current `README.md` content with your remote GitHub profile.
- Updates the profile `README.md` if there are any changes.
- Pushes the updated `README.md` to your GitHub repository.

---

## Example Output

Here's an example of the output generated for a GitHub profile:

# Hi, I'm SyntaxSkater 👋

Welcome to my GitHub profile! Here's a snapshot of my public repositories:

## github-readme-auto-update
**Description:** Automatically updates my Github profile README so I don't have to.

**Languages:** Python

**Last Updated:** 2024-12-31

---

## SyntaxSkater
**Description:** Config files for my GitHub profile.

**Languages:** No languages detected

**Last Updated:** 2024-12-31

---

# How to Use
## Prerequisites
Python Installed: Ensure you have Python 3.8 or higher installed on your machine.
GitHub Token: Create a GitHub Personal Access Token with the following permissions:
repo (for accessing private repositories, if needed)
user (to fetch profile data)
Steps to Set Up
Clone the Repository:

```bash
git clone https://github.com/SyntaxSkater/github-readme-auto-update.git
cd github-readme-auto-update
```

Install Dependencies: Install the required Python libraries using pip:

```bash
pip install -r requirements.txt
```

Set Up Your GitHub Token: Add your GitHub token as an environment variable:

#### On Windows:
```bash
setx GITHUB_TOKEN "your_github_token_here"
```
#### On macOS/Linux:
```bash
export GITHUB_TOKEN="your_github_token_here"
```
### Customize the Script: Update the GITHUB_USERNAME in update_readme.py to your GitHub username:

```python
GITHUB_USERNAME = "YourGitHubUsername"
```
### Run the Script: Execute the script to generate and push your profile README.md:

```bash
python update_readme.py
```

---

## Advanced Customization
If you want to customize the output or modify how the script works, you can edit the following sections in update_readme.py:

### Profile Content:
Modify the generate_readme_content function to customize how your profile's README.md is structured.

### Repository Filters:
Update the get_github_activity function to filter repositories by specific criteria (e.g., visibility, topics, etc.).

---

## Contributing
Feel free to fork this repository and contribute! Submit a pull request with your changes, and I'll review them.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
