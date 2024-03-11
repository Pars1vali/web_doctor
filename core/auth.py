from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from httpx_oauth.clients.google import GoogleOAuth2
import asyncio, datetime, streamlit as st

from google_auth_oauthlib.flow import Flow
flow = Flow.from_client_secrets_file(
        'core/client_secret_public.json',
        scopes=[
            "profile",
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
            "https://www.googleapis.com/auth/fitness.sleep.read"
            ,
        ],
    )
# from dotenv import load_dotenv
# https://frankie567.github.io/httpx-oauth/oauth2/
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
access_token = None


async def request_fit_data():
    credentials = Credentials(access_token, refresh_token="ff", token_uri="f", client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    fitness_store = build('fitness', 'v1', credentials=credentials)

    # Определяем параметры запроса для получения данных о шагах
    data_type_name = 'com.google.step_count.delta'
    data_source_id = 'derived:com.google.step_count.delta:com.google.android.gms:estimated_steps'
    data = {
        'aggregateBy': [{'dataTypeName': data_type_name, 'dataSourceId': data_source_id}],
        'bucketByTime': {'durationMillis': 24 * 60 * 60 * 1000},
        'startTimeMillis': int((datetime.datetime.now() - datetime.timedelta(days=20)).timestamp()) * 1000,
        'endTimeMillis': int(datetime.datetime.now().timestamp()) * 1000
    }



    # Получаем агрегированные данные о шагах
    result = fitness_store.users().dataset().aggregate(userId='me', body=data).execute()

    return result
    # Возвращаем результат в формате JSON
    # return jsonify(result)

def get_login():
    # flow.redirect_uri = 'https://web-doctor.streamlit.app/client-account'#'http://localhost:8501/client-account'
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    return authorization_url

def get_token():
    state = st.query_params.get("state")
    code = st.query_params.get("code")
    scope_str = st.query_params.get("scope")
    scope_dict = scope_str.split(" ")
    for i in range(len(scope_dict)):
        if i != len(scope_dict)-1:
            scope_dict[i] += "%20"
    scope = "".join(scope_dict)
    authuser = st.query_params.get("authuser")
    prompt = st.query_params.get("prompt")

    authorization_response = f"http://localhost:8501/client-account?state={state}&code={code}&scope={scope}&authuser={authuser}&prompt={prompt}"
    st.write(authorization_response)
    # data = authorization_response
    # st.write(data)
    # authuser prompt code scope
    # tokens = flow.fetch_token(authorization_response=authorization_response)
    # st.write(tokens)
    # return tokens

    return "developing"
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
    global access_token
    client: GoogleOAuth2 = GoogleOAuth2(CLIENT_ID, CLIENT_SECRET)
    # get the code from the url
    code = st.query_params.get_all('code')
    token = asyncio.run(get_access_token(
        client, REDIRECT_URI, code))
    user_id, user_email = asyncio.run(
        get_email(client, token['access_token']))
    access_token = token
    return user_id, user_email, token