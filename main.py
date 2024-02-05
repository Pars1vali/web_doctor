import streamlit as st
import net


def print_hi(name):
    st.title("Войти")
    login = st.text_input(label="Логин")
    password = st.text_input(label="Пароль", type="password")
    login_btn = st.button(label="Войти", type="primary")
    if(login_btn):
        st.write(net.Client.authentication(login, password))
        net.Client.url



if __name__ == '__main__':
    print_hi('PyCharm')
