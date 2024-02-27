import streamlit as st
from st_pages import Page, show_pages, hide_pages

show_pages([
    Page("pages/account.py", "Личный кабинет"),
    Page("pages/clients.py", "Клиенты"),
    Page("main.py","Выйти")
])

st.title("Личный кабинет")