
import base64
import requests

# OpenAI API Key
api_key = "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"

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "D:\\0135.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

payload = {
  "model": "gpt-4-vision-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Provide as much detail as possible about the description of the man and the surroundings in this photo. Pay special attention to the description of facial features and haircut. It is important to describe in detail that the haircut is very short"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ],
  "max_tokens": 4096
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

answer = response.json()

content = answer["choices"][0]["message"]["content"]


content = "3D cartoon gentleman with a confident smile, standing at an angle, wearing a light blue upper-body garment, with fair eye color, oval-shaped eyes. The texture of the cartoon should reflect a velvety finish, and the style should emulate a well-groomed, bald head. Holding a notebook  with green letter d. Include text in a 3D rendering style, suitable for typography or illustration, to be used in a painting, photo, poster, or 3D rendered image."


from openai import OpenAI
client = OpenAI(api_key = "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")

response = client.images.generate(
  model="dall-e-3",
  prompt=content,
  size="1024x1024",
  quality="hd",
  n=1,
)

image_url = response.data[0].url


print(image_url)











