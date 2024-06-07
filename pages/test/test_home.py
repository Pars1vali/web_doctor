from streamlit.testing.v1 import AppTest

def test_button_click():
    at = AppTest.from_file("home.py").run()
    at.button[0].click().run()
    assert not at.exception()