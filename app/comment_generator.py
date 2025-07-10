import re

def generate_comments(llm_outputs):
    comments = []

    for review in llm_outputs:
        file = review["file"]
        lines = review["raw_response"].split("\n")

        for i, line in enumerate(lines):
            # Very basic logic: attach one comment per problem line (can improve later)
            if "Rule ID:" in line:
                rule_match = re.search(r"Rule ID:\s*(\S+)", line)
                rule_id = rule_match.group(1) if rule_match else "UNKNOWN"

                code_line = lines[i + 2] if i + 2 < len(lines) else ""
                suggestion = lines[i + 3] if i + 3 < len(lines) else ""

                comments.append({
                    "path": file,
                    "line": i + 1,  # approximate (improve with better parser)
                    "body": f"⚠️ **Violation** ({rule_id}):\n{line}\n\n**Suggestion:**\n```java\n{code_line}\n{suggestion}\n```"
                })

    return comments
