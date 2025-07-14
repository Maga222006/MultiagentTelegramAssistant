from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from timezonefinder import TimezoneFinder
from langchain_core.tools import tool
from dotenv import load_dotenv
from agents.web_search import graph
from geopy import Nominatim
from github import Github
import datetime
import pytz
import os
load_dotenv()

user_id: str
yahoo = YahooFinanceNewsTool()
tf = TimezoneFinder()
geolocator = Nominatim(user_agent="my_geocoder")
weekday_mapping = ("Monday", "Tuesday",
                   "Wednesday", "Thursday",
                   "Friday", "Saturday",
                   "Sunday")

@tool
def create_repo(repo_name: str, private: bool = False):
    """Creates a GitHub repository with the given repo_name."""
    github = Github(os.getenv('GITHUB_TOKEN'))
    user = github.get_user()
    repo = user.create_repo(repo_name, private=private)
    return f"Repository '{repo_name}' created successfully!"

@tool
def commit_file_to_repo(repo_name: str, file_path: str, file_contents: str):
    """Adds a new file to the GitHub repository or updates the existing one."""
    github = Github(os.getenv('GITHUB_TOKEN'))
    user = github.get_user()
    repo = user.get_repo(repo_name)

    try:
        # Check if file exists
        file = repo.get_contents(file_path)
        sha = file.sha
        repo.update_file(file_path, "Updating file", file_contents, sha)
        return f"File '{file_path}' updated successfully in '{repo_name}'."
    except:
        repo.create_file(file_path, "Adding new file", file_contents)
        return f"File '{file_path}' created successfully in '{repo_name}'."

@tool
def read_file(repo_name: str, file_path: str):
    """Reads the content of a file from a GitHub repository."""
    github = Github(os.getenv('GITHUB_TOKEN'))
    user = github.get_user()
    repo = user.get_repo(repo_name)

    try:
        file = repo.get_contents(file_path)
        return file.decoded_content.decode('utf-8')
    except:
        return f"File '{file_path}' not found in '{repo_name}'."

@tool
def list_repos():
    """Lists all repositories owned by the authenticated GitHub user."""
    github = Github(os.getenv('GITHUB_TOKEN'))
    user = github.get_user()

    try:
        repos = user.get_repos()
        repo_names = [repo.name for repo in repos]
        return f"Repositories: {', '.join(repo_names)}"
    except:
        return "Unable to fetch repositories."

@tool
def list_files(repo_name: str):
    """Lists all files in the GitHub repository."""
    github = Github(os.getenv('GITHUB_TOKEN'))
    user = github.get_user()
    repo = user.get_repo(repo_name)

    try:
        files = repo.get_contents("")
        file_list = [file.name for file in files]
        return f"Files in '{repo_name}': {', '.join(file_list)}"
    except:
        return f"Unable to fetch files from repository '{repo_name}'."

@tool
def delete_file(repo_name: str, file_path: str):
    """Deletes a file from the GitHub repository."""
    github = Github(os.getenv('GITHUB_TOKEN'))
    user = github.get_user()
    repo = user.get_repo(repo_name)

    try:
        file = repo.get_contents(file_path)
        sha = file.sha
        repo.delete_file(file_path, "Deleting file", sha)
        return f"File '{file_path}' deleted successfully from '{repo_name}'."
    except:
        return f"File '{file_path}' not found in '{repo_name}'."


@tool
def list_branches(repo_name: str):
    """Lists all branches in a GitHub repository."""
    github = Github(os.getenv('GITHUB_TOKEN'))
    user = github.get_user()
    repo = user.get_repo(repo_name)

    try:
        branches = repo.get_branches()
        branch_names = [branch.name for branch in branches]
        return f"Branches in '{repo_name}': {', '.join(branch_names)}"
    except:
        return f"Unable to fetch branches from repository '{repo_name}'."


@tool
def create_branch(repo_name: str, branch_name: str):
    """Creates a new branch in a GitHub repository."""
    github = Github(os.getenv('GITHUB_TOKEN'))
    user = github.get_user()
    repo = user.get_repo(repo_name)

    try:
        main_branch = repo.get_branch("main")  # assuming the default branch is named 'main'
        repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=main_branch.commit.sha)
        return f"Branch '{branch_name}' created successfully in '{repo_name}'."
    except:
        return f"Unable to create branch '{branch_name}' in '{repo_name}'."


@tool
def web_search(query: str):
    """Get web search results for the given query."""
    response = graph.invoke({"question": query})
    return response['answer']


@tool
def current_time(location: str = None):
    """Get the current time for a location or current position."""
    global tf, geolocator, weekday_mapping
    location_data = geolocator.geocode(location) if location else None
    timezone = pytz.timezone(tf.timezone_at(lat=location_data.latitude, lng=location_data.longitude))
    return f"Location: {location.capitalize() if location else os.getenv('LOCATION')}; Current Date and Time: {datetime.datetime.now(timezone).strftime('%Y-%m-%d %H:%M')}, {weekday_mapping[datetime.datetime.now().weekday()]}."

@tool
def weather(location: str = None):
    """Get the current weather for a location or current position."""
    return OpenWeatherMapAPIWrapper().run(location=location)

coding_tools=[web_search, create_repo, create_branch, commit_file_to_repo, read_file, list_files, list_repos, list_branches, delete_file]
researcher_tools=[yahoo, web_search, current_time, weather]
