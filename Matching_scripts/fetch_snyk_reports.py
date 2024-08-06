import requests
import json
import os

snyk_token = os.getenv('SNYK_TOKEN')
org_id = os.getenv('SNYK_ORG_ID')
project_ids = os.getenv('SNYK_PROJECT_IDS').split(',')  # Assuming comma-separated project IDs

api_url = "https://snyk.io/api/v1"

headers = {
    "Authorization": f"token {snyk_token}",
    "Content-Type": "application/json"
}

def get_project_issues(project_id):
    url = f"{api_url}/org/{org_id}/project/{project_id}/issues"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve issues for project {project_id}: {response.status_code}")
        return None

all_issues = []

for project_id in project_ids:
    issues = get_project_issues(project_id)
    if issues:
        output_file = f'snyk_project_{project_id}_issues.json'
        with open(output_file, 'w') as file:
            json.dump(issues, file, indent=2)
        print(f"Snyk project issues for {project_id} saved to {output_file}")
        all_issues.append(issues)
    else:
        print(f"No issues found or failed to retrieve issues for project {project_id}.")

merged_file = 'merged_snyk_project_issues.json'
with open(merged_file, 'w') as file:
    json.dump(all_issues, file, indent=2)

print(f"All Snyk project issues merged into {merged_file}")
