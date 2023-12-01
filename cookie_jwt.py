import requests
import jwt

# Set the URL for authentication
auth_url = "https://example.com/authenticate"

# Set your credentials (replace with your actual credentials)
username = "your_username"
password = "your_password"

# Create a session
session = requests.Session()

# Perform login and retrieve cookies
login_payload = {"username": username, "password": password}
response = session.post(auth_url, data=login_payload)

# Check if login was successful
if response.status_code == 200:
    print("Login successful")

    # Extract and print cookies
    cookies = session.cookies.get_dict()
    print("Cookies:", cookies)

    # Extract JWT from the response (adjust this based on the actual response structure)
    jwt_token = response.json().get("jwt")
    print("JWT Token:", jwt_token)

    # Save cookies and JWT to variables for later use
    saved_cookies = cookies
    saved_jwt = jwt_token

    # Now you can use the session object for subsequent requests, and include the JWT in the headers if required
    # For example:
    # headers = {"Authorization": f"Bearer {saved_jwt}"}
    # response = session.get("https://example.com/api/resource", headers=headers)

else:
    print("Login failed. Status code:", response.status_code)
    print("Response content:", response.text)