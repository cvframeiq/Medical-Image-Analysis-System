import requests
import base64
import json
import os

# Function to send image and question to OpenRouter's GPT-4o
def get_vqa_answer(image_path, question):
    # Safety check
    if not os.path.exists(image_path):
        return " Image not found."
    if not question.strip():
        return " No question provided."

    try:
        # Encode image to base64
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")

        # API headers
        headers = {
            "Authorization": "Bearer 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",
            "Content-Type": "application/json"
        }

        # Payload for GPT-4o with image + question
        payload = {
            "model": "openai/gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            "max_tokens": 300
        }

        # Send POST request
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )

        # Parse response
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            print(f"[Error] Status Code: {response.status_code}")
            print(response.text)
            return f" API Error: {response.status_code} – see console."

    except Exception as e:
        print(f"[Exception] {e}")
        return " Failed to process the image or send the request."

