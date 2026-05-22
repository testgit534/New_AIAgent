from openai import OpenAI

def generate_output(prompt: str, api_key: str) -> str:
    if not api_key:
        raise ValueError("API key is required")

    client = OpenAI(api_key=api_key)

    try:
        response = client.responses.create(
            model="gpt-4.1",
            input=[
                {
                    "role": "system",
                    "content": """
You are a senior QA engineer.

You MUST generate extensive and comprehensive QA coverage.

For manual testing:
- Generate large volume regression coverage
- Generate minimum 30 to 40 test cases
- Continue generating until all meaningful scenarios are covered
- Include positive, negative, edge, validation, UI, accessibility, security, usability, and navigation scenarios
- Avoid stopping early
- Avoid summarization
"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_output_tokens=4000,
        )

        return response.output[0].content[0].text.strip()

    except Exception as e:
        print("OpenAI Error:", str(e))
        return f"Error: {str(e)}"