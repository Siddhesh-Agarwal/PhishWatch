from typing import Any
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
    res: dict[Any, Any] = requests.post(API_URL, json={"url": URL}).json()
    # st.json(res)
    intensity_to_score: dict[str, int] = {
        "high": 3,
        "medium": 2,
        "low": 1,
    }
    reasons = res["reasons"]
    score: int = sum(intensity_to_score[reason["intensity"]] for reason in reasons)
    st.markdown(f"**Phishing Score:** {score}")
    if st.checkbox(label="Show Response"):
        st.json(res)

    if st.checkbox("Show Reasons"):
        for reason in reasons:
            if reason["intensity"] == "high":
                st.error(reason["reason"])
            elif reason["intensity"] == "medium":
                st.warning(reason["reason"])
            else:
                st.info(reason["reason"])
