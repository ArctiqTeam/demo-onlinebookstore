import requests
import json
import os

repo_owner = os.getenv('GITHUB_REPOSITORY_OWNER')
repo_name = os.getenv('GITHUB_REPOSITORY').split('/')[-1]
token = os.getenv('CODEQL_TOKEN')

api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/dependabot/alerts"

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

def extract_vulnerability_info(alert):
    security_advisory = alert.get('security_advisory', {})
    return {
        "ghsa_id": security_advisory.get("ghsa_id"),
        "cve_id": security_advisory.get("cve_id"),
        "summary": security_advisory.get("summary"),
        "description": security_advisory.get("description"),
        "severity": security_advisory.get("severity"),
        "identifiers": [
            {
                "value": identifier.get("value"),
                "type": identifier.get("type")
            } for identifier in security_advisory.get("identifiers", [])
        ]
    }

response = requests.get(api_url, headers=headers)
alerts = response.json()

vulnerabilities = [extract_vulnerability_info(alert) for alert in alerts]

output_file = 'dependabot_vulnerabilities.json'
with open(output_file, 'w') as file:
    json.dump(vulnerabilities, file, indent=2)

print(f"Extracted vulnerabilities saved to {output_file}")
