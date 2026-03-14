import base64
import json
import os
import re

from dotenv import load_dotenv
from openai import OpenAI

from utils.agent_decorator import agent
from prompts.vision_locator_prompt import build_prompt

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def parse_json(text):
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception:
        return None


@agent("Vision Locator Agent")
def vision_locator_agent(state):

    elements = state.get("interactive_elements", [])
    screenshot_path = state.get("screenshot_path")

    screenshot = encode_image(screenshot_path)

    results = []

    for element in elements[:50]:  # limit to avoid huge token usage

        prompt = build_prompt(element)

        try:

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                temperature=0,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a senior QA automation engineer generating stable UI locators."
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{screenshot}"
                                }
                            }
                        ]
                    }
                ]
            )

            response_text = response.choices[0].message.content

            parsed = parse_json(response_text)

            if parsed:
                results.append(parsed)

        except Exception as e:
            print(f"⚠️ Failed to process element: {e}")

    state["final_output"] = results

    return state