import os
import requests
import webbrowser

def upload_media(file_path, access_token):
    url = "https://api.pinterest.com/v5/media"
    headers = {"Authorization": f"Bearer {access_token}"}
    with open(file_path, "rb") as file:
        files = {"media": file}
        response = requests.post(url, headers=headers, files=files)
    if response.ok:
        data = response.json()
        return data.get("id")
    else:
        print("Error uploading media:")
        print(response.text)
        return None

def create_pin(board_id, media_id, caption, access_token):
    url = "https://api.pinterest.com/v5/pins"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {
        "board_id": board_id,
        "media_source": {"media_id": media_id},
        "description": caption  # This is where your caption goes
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.ok:
        print("Pin created successfully!")
        print("Response:", response.json())
    else:
        print("Error creating pin:")
        print("Status code:", response.status_code)
        print("Response:", response.text)

if __name__ == "__main__":
    # Get the access token from the environment variable
    ACCESS_TOKEN = os.getenv("PINTEREST_ACCESS_TOKEN")
    if not ACCESS_TOKEN:
        print("Access token not found. Please ensure the credentials file is sourced correctly.")
        exit(1)

    FILE_PATH = "generated_images/couch.png"  # Replace with your actual file path
    BOARD_ID = "your_board_id_here"            # Replace with your target board ID
    CAPTION = "This is my caption for the pin!"  # Replace with your desired caption

    media_id = upload_media(FILE_PATH, ACCESS_TOKEN)
    if media_id:
        create_pin(BOARD_ID, media_id, CAPTION, ACCESS_TOKEN)

# Replace with your actual App ID and redirect URI
APP_ID = os.getenv("PINTEREST_APP_ID")
if not APP_ID:
    print("App ID not found. Please ensure the credentials file is sourced correctly.")
    exit(1)

REDIRECT_URI = "http://localhost:8085/"
SCOPE = "read_public,write_public"  # Adjust scopes as needed

# Construct the authorization URL
auth_url = (
    f"https://www.pinterest.com/oauth/?response_type=code"
    f"&client_id={APP_ID}"
    f"&redirect_uri={REDIRECT_URI}"
    f"&scope={SCOPE}"
)

# Open the authorization URL in the default web browser
webbrowser.open(auth_url)
