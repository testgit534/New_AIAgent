import pandas as pd
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
import os
from flask import send_file

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
from flask_cors import CORS
from openpyxl import Workbook
from flask import send_file
import json
import os

from prompt_builder import build_url_prompt, build_ac_prompt
from llm_client import generate_output

app = Flask(__name__)
CORS(app)

AGENT_NAME = "Suraj QA Agent"


api_key = os.getenv("OPENAI_API_KEY")

@app.route("/generate", methods=["POST"])
def generate():

    try:

        data = request.json

        mode = data.get("mode")

        output_type = data.get("output_type", "manual")

        playwright_language = data.get("playwright_language", "JavaScript")

        api_key = OPENAI_API_KEY

        # URL MODE
        if mode == "url":

            url = data.get("url")

            prompt = build_url_prompt(url, "", {})

        # ACCEPTANCE CRITERIA MODE
        elif mode == "ac":

            ac_text = data.get("ac_text")

            prompt = build_ac_prompt(ac_text)

        else:

            return jsonify({"error": "Invalid mode"}), 400

        # PLAYWRIGHT MODE
        if output_type == "playwright":

            prompt += f"""

Generate ONLY Playwright {playwright_language} code.

IMPORTANT:
- Do not generate manual test cases
- Do not generate JSON
- Do not generate explanations
- Do not generate markdown
- Return executable Playwright code only

"""

            result = generate_output(prompt, api_key)

            return jsonify({"agent_name": AGENT_NAME, "manual": [], "code": result})

        # MANUAL MODE
        else:

            prompt += """

Generate ONLY manual test cases JSON.

IMPORTANT RULES:
- Return ONLY valid JSON
- Do not generate explanations
- Do not generate markdown
- Do not generate Playwright code
- Do not generate headings
- Do not generate extra text

STRICT JSON FORMAT:

[
    {
        "tc_id": "TC_LOGIN_001",
        "scenario": "Verify successful login",
        "steps": [
            "Enter valid username",
            "Enter valid password",
            "Click Login"
        ],
        "expected_result": "User should login successfully"
    }
]

"""

            result = generate_output(prompt, api_key)

            manual_text = result.strip()

            manual_text = manual_text.replace("```json", "")

            manual_text = manual_text.replace("```", "")

            manual_text = manual_text.strip()

            print("========== RAW AI OUTPUT ==========")
            print(manual_text)
            print("===================================")

            try:

                manual = json.loads(manual_text)

                print("===================================")
                print("TOTAL TEST CASES:", len(manual))

                for tc in manual:

                    print(tc.get("tc_id"))

                print("===================================")

                return jsonify({"agent_name": AGENT_NAME, "manual": manual, "code": ""})

            except Exception as e:

                print("JSON ERROR:", e)

                print(manual_text)

                return (
                    jsonify(
                        {"error": "AI returned invalid JSON", "raw_output": manual_text}
                    ),
                    500,
                )

    except Exception as e:

        return jsonify({"error": str(e)}), 500


@app.route("/export-excel", methods=["POST"])
def export_excel():

    try:

        data = request.json

        manual = data.get("manual", [])

        df = pd.DataFrame(manual)

        df["action"] = df["action"].apply(
            lambda steps: "\n".join(steps) if isinstance(steps, list) else steps
        )

        column_order = [
            "tc_id",
            "test_case_name",
            "action",
            "expected_result",
            "priority",
            "scenario_type",
        ]

        df = df.reindex(columns=column_order)

        file_name = "test_cases.xlsx"

        df.to_excel(file_name, index=False)

        return send_file(file_name, as_attachment=True)

    except Exception as e:

        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return {
        "message": "Playwright AI Agent Backend Running",
        "status": "success"
    }


if __name__ == "__main__":

    app.run(debug=True, port=5000)
