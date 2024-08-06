import requests
import json
import os

def main():
    repo_owner = os.getenv('GITHUB_REPOSITORY_OWNER')
    repo_name = os.getenv('GITHUB_REPOSITORY').split('/')[1]
    github_token = os.getenv('GITHUB_TOKEN')

    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/dependabot/alerts'

    # Set up headers for authentication
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github+json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        alerts = response.json()
        
        with open('dependabot_alerts.json', 'w') as file:
            json.dump(alerts, file, indent=4)
        
        print("Dependabot alerts exported successfully.")
    else:
        print(f"Failed to retrieve alerts: {response.status_code} - {response.text}")

if __name__ == '__main__':
    main()
