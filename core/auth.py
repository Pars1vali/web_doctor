from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import streamlit as st

from google_auth_oauthlib.flow import Flow

flow = Flow.from_client_secrets_file(
# 'core/client_secret.json',
    'core/client_secret_public.json',
    scopes=["openid",
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile',
            "https://www.googleapis.com/auth/fitness.location.read",
            "https://www.googleapis.com/auth/fitness.activity.read",
            "https://www.googleapis.com/auth/fitness.blood_glucose.read",
            "https://www.googleapis.com/auth/fitness.blood_pressure.read",
            "https://www.googleapis.com/auth/fitness.body.read",
            "https://www.googleapis.com/auth/fitness.body_temperature.read",
            "https://www.googleapis.com/auth/fitness.heart_rate.read",
            "https://www.googleapis.com/auth/fitness.nutrition.read",
            "https://www.googleapis.com/auth/fitness.oxygen_saturation.read",
            "https://www.googleapis.com/auth/fitness.reproductive_health.read",
            "https://www.googleapis.com/auth/fitness.sleep.read"
            ],
)
# flow.redirect_uri = 'http://localhost:8501/client-account'

flow.redirect_uri = 'https://web-doctor.streamlit.app/client-account'

def get_login():
    authorization_url, state = flow.authorization_url(
        access_type='offline')  # ,        include_granted_scopes='true')
    return authorization_url


def _get_parameters():
    state = st.query_params.get("state")
    code = st.query_params.get("code")
    scope_str = st.query_params.get("scope")
    scope_dict = scope_str.split(" ")
    for i in range(len(scope_dict)):
        if i != len(scope_dict) - 1:
            scope_dict[i] += "%20"
    scope = "".join(scope_dict)
    authuser = st.query_params.get("authuser")
    prompt = st.query_params.get("prompt")
    return state, code, scope, authuser, prompt


# @st.cache_resource
def _get_tokens(state, code, scope, authuser, prompt):
    authorization_response = f"https://web-doctor.streamlit.app/client-account?state={state}&code={code}&scope={scope}&authuser={authuser}&prompt={prompt}"
    tokens = flow.fetch_token(authorization_response=authorization_response)
    return tokens

def get_token():
    state, code, scope, authuser, prompt = _get_parameters()
    token = _get_tokens(state, code, scope, authuser, prompt)
    # st.write("token - ", token)
    return token #token["access_token"] #, token["refresh_token"]


def get_email(access_token):#, refresh_token):
    creds = Credentials(token=access_token,
                        # refresh_token=refresh_token,
                        client_id="169068403601-uhgrr6frls1oc1idu9v49v0dedjsla8p.apps.googleusercontent.com",
                        client_secret="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",
                        token_uri="https://oauth2.googleapis.com/tokenhttps://oauth2.googleapis.com/token")
    user_info_service = build('oauth2', 'v2', credentials=creds)
    try:
        user_info = user_info_service.userinfo().get().execute()
    except Exception as e:
        user_info = None
        print(e)
        st.warning("Произошла ошибка на сервере Google")
    return user_info
