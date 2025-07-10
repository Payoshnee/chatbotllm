import openai
from app.utils import load_config
import os

# You can also load from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

def review_with_llm(changed_java_files, config):
    prompt_template_path = os.path.join(os.path.dirname(__file__), "../rules/prompt_template.txt")
    with open(prompt_template_path, "r", encoding="utf-8") as f:
        base_prompt = f.read()

    reviews = []

    for filename, lines in changed_java_files.items():
        code_snippet = "\n".join([line for _, line in lines])
        prompt = base_prompt + f"\n\nFile: {filename}\n\nCode:\n{code_snippet}"

        try:
            response = openai.ChatCompletion.create(
                model=config["llm"]["model"],
                temperature=config["llm"]["temperature"],
                max_tokens=config["llm"]["max_tokens"],
                messages=[
                    {"role": "system", "content": "You are a senior Java code reviewer following internal firm guidelines."},
                    {"role": "user", "content": prompt}
                ]
            )
            reviews.append({
                "file": filename,
                "raw_response": response.choices[0].message.content.strip()
            })
        except Exception as e:
            reviews.append({
                "file": filename,
                "raw_response": f"Error from LLM: {str(e)}"
            })

    return reviews
