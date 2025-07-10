import yaml
import os

def extract_pr_info(payload):
    return {
        "repo_url": payload["repository"]["clone_url"],
        "base_sha": payload["pull_request"]["base"]["sha"],
        "head_sha": payload["pull_request"]["head"]["sha"]
    }

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)
