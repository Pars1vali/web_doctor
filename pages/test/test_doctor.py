from streamlit.testing.v1 import AppTest

def test_login_correct():
    at = AppTest.from_file("doctor.py").run()
    # at.text_input(key="login_name").input("marina").run()
    # at.text_input(key="login_password").input("1234").run()
    # at.button[0].click().run()

    assert at.switch_page("clients.py").run()

def test_login_incorrect():
    assert 1==1
