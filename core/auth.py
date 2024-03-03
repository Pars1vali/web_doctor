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

# CLIENT_ID = "169068403601-mshu43a5uvutk61ubberhps94r60n6p7.apps.googleusercontent.com"#os.environ['CLIENT_ID']
# CLIENT_SECRET = "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"#os.environ['CLIENT_SECRET']
# REDIRECT_URI = "http://localhost:8501"#os.environ['REDIRECT_URI']

CLIENT_ID = "169068403601-gt219934qaiqm1mp5b1aohf9dusk7fao.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:8501/client-account"#os.environ['REDIRECT_URI']



async def get_authorization_url(client: GoogleOAuth2, redirect_uri: str):
    authorization_url = await client.get_authorization_url(redirect_uri, scope=["profile", "email"])
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


def display_user() -> void:
    client: GoogleOAuth2 = GoogleOAuth2(CLIENT_ID, CLIENT_SECRET)
    # get the code from the url
    code = st.experimental_get_query_params()['code']
    token = asyncio.run(get_access_token(
        client, REDIRECT_URI, code))
    user_id, user_email = asyncio.run(
        get_email(client, token['access_token']))
    st.write(
        f"You're logged in as {user_email} and id is {user_id}")