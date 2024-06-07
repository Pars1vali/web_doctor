from streamlit.testing.v1 import AppTest

def test_search_client():
    at = AppTest.from_file("clients.py").run()
    at.