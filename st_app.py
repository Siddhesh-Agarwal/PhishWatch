import streamlit as st
import requests

st.set_page_config(
    page_title="PhishWatch",
    page_icon="🐟",
    layout="centered",
    initial_sidebar_state="auto",
)

st.title("PhishWatch")

URL: str = st.text_input(
    label="Enter URL",
    help="Enter the URL to check for phishing",
    placeholder="https://www.google.com",
)

API_URL = "http://localhost:8000/api/check"

if st.button("Submit"):
    res: requests.Response = requests.post(API_URL, json={"url": URL})
    st.json(res.json())
