from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# initialize flask app
app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Haiku Generator Endpoint
@app.route('/generate-haiku', methods=['POST'])
def generate_haiku():
    try:
        data = request.json
        topic = data.get('topic', 'nature')

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a haiku generator."},
                {"role": "user", "content": f"Write a haiku about {topic}."}
            ],
            max_tokens=50,
            temperature=0.7
        )

        # Extract and print the response
        haiku = response.choices[0].message.content

        return jsonify({"haiku": haiku}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5001)
