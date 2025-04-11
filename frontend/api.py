import requests


def send_jwt_to_server(jwt_token: str):
    try:
        response = requests.post("http://127.0.0.1:5000/api/auth", json={"token": jwt_token})
        return response.status_code, response.json()
    except Exception as e:
        return 500, {"error": str(e)}
