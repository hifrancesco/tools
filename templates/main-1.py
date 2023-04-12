"""
use a while loop to retrieve all workflows for every repository. Here's an example script that retrieves all workflows for a given user's repositories
"""

import requests

# GitHub API endpoint for retrieving all repositories for a user
repo_url = "https://api.github.com/users/{username}/repos"

# Replace {username} with the appropriate value for your user
repo_url = repo_url.format(username="<username>")

# Add a personal access token to authenticate the request
headers = {
    "Authorization": "Token <your_personal_access_token>"
}

# Make the GET request to retrieve the repositories
repo_response = requests.get(repo_url, headers=headers)

# Check the status code of the response
if repo_response.status_code == 200:
    # Retrieve the repository data from the response
    repositories = repo_response.json()
    for repository in repositories:
        # GitHub API endpoint for retrieving all workflows for a repository
        workflow_url = "https://api.github.com/repos/{owner}/{repo}/actions/workflows"

        # Replace {owner} and {repo} with the appropriate values for the repository
        workflow_url = workflow_url.format(owner=repository["owner"]["login"], repo=repository["name"])

        # Set the `page` and `per_page` parameters to control pagination
        params = {
            "page": 1,
            "per_page": 30
        }

        # Use a while loop to retrieve all pages of results
        while True:
            # Make the GET request to retrieve the workflows
            workflow_response = requests.get(workflow_url, headers=headers, params=params)

            # Check the status code of the response
            if workflow_response.status_code == 200:
                # Retrieve the workflow data from the response
                workflows = workflow_response.json()

                # Process the workflows
                for workflow in workflows:
                    print(workflow["id"], workflow["name"])

                # Check if there are more pages of results
                if "next" not in workflow_response.links:
                    break
                else:
                    # Increment the page parameter for the next iteration of the loop
                    params["page"] += 1
            else:
                # Handle any error responses from the API
                print("Failed to retrieve workflows for repository {}:".format(repository["full_name"]), workflow_response.text)
                break
else:
    # Handle any error responses from the API
    print("Failed to retrieve repositories:", repo_response.text)
