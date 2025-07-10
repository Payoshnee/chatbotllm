import os
import subprocess
import tempfile
from unidiff import PatchSet

def get_changed_java_files(pr_info):
    repo_url = pr_info["repo_url"]
    base_sha = pr_info["base_sha"]
    head_sha = pr_info["head_sha"]
# def get_changed_java_files(pr_info):
#     # Bypassing Git – returning dummy Java file for testing
#     return {
#         "HelloWorld.java": [
#             (10, 'public class HelloWorld {'),
#             (11, '    public void sayHello() {'),
#             (12, '        System.out.println("Hello, world!");'),
#             (13, '    }'),
#             (14, '}')
#         ]
#     }

    with tempfile.TemporaryDirectory() as tmpdir:
        subprocess.run(["git", "clone", repo_url, tmpdir], check=True)

        os.chdir(tmpdir)
        subprocess.run(["git", "fetch", "origin", base_sha, head_sha], check=True)
        subprocess.run(["git", "checkout", head_sha], check=True)

        diff = subprocess.run(
            ["git", "diff", f"{base_sha}..{head_sha}"],
            capture_output=True,
            text=True,
            check=True
        ).stdout

        patch = PatchSet(diff)

        java_files = {}
        for patched_file in patch:
            if patched_file.path.endswith(".java"):
                modified_lines = []
                for hunk in patched_file:
                    for line in hunk:
                        if line.is_added:
                            modified_lines.append((line.target_line_no, line.value.strip()))
                java_files[patched_file.path] = modified_lines

        return java_files
