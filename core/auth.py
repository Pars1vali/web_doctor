# IMPORTING LIBRARIES
import os
from numpy import void
import streamlit as st
import asyncio
# https://frankie567.github.io/httpx-oauth/oauth2/
from httpx_oauth.clients.google import GoogleOAuth2
# from dotenv import load_dotenv
#
# load_dotenv('.env')

# CLIENT_ID = os.environ['CLIENT_ID']
# CLIENT_SECRET = os.environ['CLIENT_SECRET']
# REDIRECT_URI = os.environ['REDIRECT_URI']

# CLIENT_ID = "169068403601-gt219934qaiqm1mp5b1aohf9dusk7fao.apps.googleusercontent.com"
# CLIENT_SECRET = "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"
# REDIRECT_URI = "http://localhost:8501/client-account"#os.environ['REDIRECT_URI']

CLIENT_ID = "169068403601-uhgrr6frls1oc1idu9v49v0dedjsla8p.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:8501/client-account"#os.environ['REDIRECT_URI']


async def get_authorization_url(client: GoogleOAuth2, redirect_uri: str):
    authorization_url = await client.get_authorization_url(redirect_uri, scope=["profile",
                                                                                "email",
                                                                                "https://www.googleapis.com/auth/fitness.activity.read",
                                                                                "https://www.googleapis.com/auth/fitness.blood_glucose.read",
                                                                                "https://www.googleapis.com/auth/fitness.blood_pressure.read",
                                                                                "https://www.googleapis.com/auth/fitness.body.read",
                                                                                "https://www.googleapis.com/auth/fitness.body_temperature.read",
                                                                                "https://www.googleapis.com/auth/fitness.heart_rate.read",
                                                                                "https://www.googleapis.com/auth/fitness.location.read",
                                                                                "https://www.googleapis.com/auth/fitness.nutrition.read",
                                                                                "https://www.googleapis.com/auth/fitness.oxygen_saturation.read",
                                                                                "https://www.googleapis.com/auth/fitness.reproductive_health.read",
                                                                                "https://www.googleapis.com/auth/fitness.sleep.read"])
    return authorization_url


async def get_access_token(client: GoogleOAuth2, redirect_uri: str, code: str):
    token = await client.get_access_token(code, redirect_uri)
    return token


async def get_email(client: GoogleOAuth2, token: str):
    user_id, user_email = await client.get_id_email(token)
    return user_id, user_email


def get_login_str():
    client: GoogleOAuth2 = GoogleOAuth2(CLIENT_ID, CLIENT_SECRET)
    authorization_url = asyncio.run(
        get_authorization_url(client, REDIRECT_URI))
    return authorization_url
    #return f''' < a target = "_self" href = "{authorization_url}" > Google login < /a > '''


def display_user():
    client: GoogleOAuth2 = GoogleOAuth2(CLIENT_ID, CLIENT_SECRET)
    # get the code from the url
    code = st.query_params.get_all('code')
    token = asyncio.run(get_access_token(
        client, REDIRECT_URI, code))
    user_id, user_email = asyncio.run(
        get_email(client, token['access_token']))
    return user_id, user_email