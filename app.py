import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page
import requests
from streamlit_lottie import st_lottie

page = st.sidebar.selectbox("Explore or Predict", ("ML Prediction", "Explore Data"))


def load_lottieurl(url: str):    # sourcery skip: assign-if-exp, reintroduce-else
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_ML = load_lottieurl('https://lottie.host/03043152-81e4-4b9c-9cca-0714082c67d9/IUNSLXauZS.json')


if page == "ML Prediction":
    st_lottie(
        lottie_ML,
        speed=1,
        loop=True,
        height=300,
        width=500,
        key=1
    )
    show_predict_page()
else:
    show_explore_page()

