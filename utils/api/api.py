# from flask import Flask, redirect, session, request, Response
# # from ..config import GlobalConfig #Config
# from ..shared import glob_conf as config
# import requests
# import os
# import webbrowser
# import aiohttp
# import asyncio
# # Lower logging levels
# import logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

# # config = GlobalConfig()

# TWITCH_AUTH_URL = "https://id.twitch.tv/oauth2/authorize"
# TWITCH_TOKEN_URL = "https://id.twitch.tv/oauth2/token"
# TWITCH_REDIRECT_URI = "http://localhost:53847/callback"
# TWITCH_SCOPE = "chat:read chat:edit"
# TWITCH_CLIENT_ID = config.client_id
# # TWITCH_CLIENT_SECRET = config.client_secret

# app = Flask(__name__)
# app.secret_key = os.urandom(24)

# @app.route("/")
# def twitch_login():
#     twitch_auth_url = f"{TWITCH_AUTH_URL}?response_type=code&client_id={TWITCH_CLIENT_ID}&redirect_uri={TWITCH_REDIRECT_URI}&scope={TWITCH_SCOPE}"
#     return redirect(twitch_auth_url)


# @app.route("/callback")
# def twitch_callback():
#     global config
#     code = request.args.get("code")

#     token_data = {
#         "client_id": TWITCH_CLIENT_ID,
#         "client_secret": TWITCH_CLIENT_SECRET,
#         "code": code,
#         "grant_type": "authorization_code",
#         "redirect_uri": TWITCH_REDIRECT_URI,
#     }

#     headers = {"Content-Type": "application/x-www-form-urlencoded"}

#     response = requests.post(TWITCH_TOKEN_URL, data=token_data, headers=headers)
#     token_data = response.json()

#     if "access_token" in token_data:
#         session["twitch_access_token"] = token_data["access_token"]
#         refresh_token = token_data.get("refresh_token")

#         # Update the configuration
#         # twitch_config["access_token"] = token_data["access_token"]
#         config.set_val("auth.access_token", token_data["access_token"])
#         # config.access_token = token_data["access_token"]
#         if refresh_token:
#             # twitch_config["refresh_token"] = refresh_token
#             config.set_val("auth.refresh_token", refresh_token)
#             # config.refresh_token = refresh_token

#         # global_config["twitch"] = twitch_config
#         # push_config(global_config)

#         return "Twitch Access Token obtained and saved!"
#     else:
#         # file deepcode ignore XSS: Not a valid issue, no other users exist
#         return Response(
#             f"Error obtaining Twitch token: {token_data}", mimetype="text/plain"
#         )

# async def failed_auth(config_data: dict) -> None:
#     # print(config_data)
#     if config_data["auth"]["refresh_token"] is None or config_data["auth"]["refresh_token"] == "":
#         print("No refresh token, opening browser...")
#         webbrowser.open("http://localhost:53847")
#         # time.sleep(2)
#         await asyncio.sleep(2)
#         return
#     # If that statement passes, then there must be a refresh token. Use it.
#     global config
#     url = "https://id.twitch.tv/oauth2/token"
#     params = {
#         "grant_type": "refresh_token",
#         "refresh_token": config_data["auth"]["refresh_token"],
#         "client_id": config_data["auth"]["client_id"],
#         "client_secret": config_data["auth"]["client_secret"]
#     }
    
#     async with aiohttp.ClientSession() as session:
#         async with session.post(url, params=params) as response:
#             if response.status == 200:
#                 data = await response.json()
#                 # return data.get("access_token"), data.get("refresh_token")
#                 config.set_val("auth.access_token", data.get("access_token"))
#                 config.set_val("auth.refresh_token", data.get("refresh_token"))
#                 # config.access_token = data.get("access_token")
#                 # config.refresh_token = data.get("refresh_token")

            
#             else:
#                 error_data = await response.text()
#                 raise Exception(f"Failed to refresh token: {response.status} - {error_data}")
    

# def start_api(port_num: int = 53847) -> None:
#     # print("API STARTED | From utils/api/api.py")
#     app.run(port=port_num)


# if __name__ == "__main__":
#     start_api()

from flask import Flask, redirect, session, request, Response
# from ..config import GlobalConfig  # Config
from ..shared import glob_conf
import os
import hashlib
import base64
import requests
import secrets
import webbrowser
import asyncio
import aiohttp
import urllib.parse

# Lower logging levels
import logging

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

config = glob_conf

TWITCH_AUTH_URL = "https://id.twitch.tv/oauth2/authorize"
TWITCH_DEVICE_URL = "https://id.twitch.tv/oauth2/device"
TWITCH_TOKEN_URL = "https://id.twitch.tv/oauth2/token"
TWITCH_REDIRECT_URI = "http://localhost:53847/callback"
TWITCH_SCOPE = "chat:read chat:edit"
TWITCH_CLIENT_ID = config.client_id

app = Flask(__name__)
app.secret_key = os.urandom(24)


# @app.route("/")
# def twitch_login():
#     # Get device code, user code, verification uri
    


@app.route("/callback")
def twitch_callback():
    global config
    config = glob_conf

    return request.args

    code = request.args.get("access_token")
    if not code:
        return Response("Error: Missing authorization code.", mimetype="text/plain")

    token_data = {
        "client_id": TWITCH_CLIENT_ID,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": TWITCH_REDIRECT_URI,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(TWITCH_TOKEN_URL, data=token_data, headers=headers)
    token_data = response.json()

    if "access_token" in token_data:
        session["twitch_access_token"] = token_data["access_token"]
        refresh_token = token_data.get("refresh_token")

        # Update the configuration
        config.set_val("auth.access_token", token_data["access_token"])
        if refresh_token:
            config.set_val("auth.refresh_token", refresh_token)

        return "Twitch Access Token obtained and saved!"
    else:
        return Response(
            f"Error obtaining Twitch token: {token_data}", mimetype="text/plain"
        )


async def failed_auth(config_data: dict) -> None:
    global config
    config = glob_conf
    # If no refresh token, open browser to initiate authentication
    if not config_data["auth"]["refresh_token"]:
        print("No refresh token, opening browser...")
        data = {
            "client_id": config.client_id,
            "scopes": TWITCH_SCOPE
        }
        print(data)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        async with aiohttp.ClientSession() as session:
            async with session.post(TWITCH_DEVICE_URL, data=data, headers=headers) as response:
                device_data = await response.json()
        print(device_data)
        if "device_code" in device_data:
            # print("There was a device")
            device_code = device_data["device_code"]
            # user_code = device_data["user_code"]
            verification_uri = device_data["verification_uri"]
            # expires_in = device_data["expires_in"]
            # print(device_data)
            webbrowser.open(verification_uri)
            print("Opened Browser...")
            data = {
                "location": "https://your-app-domain",
                "client_id": config.client_id,
                "scopes": TWITCH_SCOPE,
                "device_code": device_code,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
            }
            print(data)
            resp_data = {}
            while resp_data.get("status") == 400 or not resp_data.get("access_token"):
                print(f"Waiting for authorization... {resp_data}")
                async with aiohttp.ClientSession() as session:
                    async with session.post(TWITCH_TOKEN_URL, data=data) as response:
                        resp_data = await response.json()
                await asyncio.sleep(1)

            if resp_data.get("access_token"):
                print(resp_data)
                config.set_val("auth.access_token", resp_data["access_token"])
                config.set_val("auth.refresh_token", resp_data["refresh_token"])
        await asyncio.sleep(2)
        print("RETURNING")
        return
    
    # If there's a refresh token, use it to request a new access token
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "grant_type": "refresh_token",
        "refresh_token": config_data["auth"]["refresh_token"],
        "client_id": config_data["auth"]["client_id"],
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    config.set_val("auth.access_token", data.get("access_token"))
                    config.set_val("auth.refresh_token", data.get("refresh_token"))
                else:
                    error_data = await response.text()
                    raise Exception(f"Failed to refresh token: {response.status} - {error_data}")
    except aiohttp.ClientError as e:
        print(f"Network error while refreshing token: {e}")


def start_api(port_num: int = 53847) -> None:
    ... # Placebo
    # app.run(port=port_num)


if __name__ == "__main__":
    start_api()
