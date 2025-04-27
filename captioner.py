import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def generate_caption(description):
    url = "https://api.fireworks.ai/inference/v1/chat/completions"
    payload = {
      "model": "accounts/sentientfoundation/models/dobby-unhinged-llama-3-3-70b-new",
      "max_tokens": 16384,
      "top_p": 1,
      "top_k": 40,
      "presence_penalty": 0,
      "frequency_penalty": 0,
      "temperature": 0.6,
      "messages": [
        {
          "role": "user",
          "content": f"""please respond with only json object with the following keys: caption, title, alt_text, tagged_topics. The caption should be a pinterest caption for an aesthetic photo of the following product from amazon. 
                          Don't make the caption seem like an ad for the product, rather focus on interior design where the product happens to be features. 
                          Mention that if they'd like the product they can click Visit Site to see it. The title should be cutesy and should suggest interior decoration inspiration, rather than advertising the product. 
                          Please also generate 2 to 3 tagged topics for the pin. Here is the product description: {description}.
                          """
        }
      ]
    }
    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json",
      "Authorization": f"Bearer {os.getenv('FIREWORKS_API_KEY')}"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    text = response.json()["choices"][0]["message"]["content"]
    json_text = text[text.find("{"):text.rfind("}")+1]
    json_out = json.loads(json_text)
    return json_out

if __name__ == "__main__":
    description = """your long description..."""
    caption = generate_caption(description)
    print(caption)
