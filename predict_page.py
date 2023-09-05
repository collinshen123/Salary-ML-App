import json
import streamlit as st
import pickle
import numpy as np
import requests
from streamlit_lottie import st_lottie


def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data


data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]


def load_lottieurl(url: str):    # sourcery skip: assign-if-exp, reintroduce-else
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_ML = load_lottieurl('https://lottie.host/03043152-81e4-4b9c-9cca-0714082c67d9/IUNSLXauZS.json')

def show_predict_page():  # sourcery skip: extract-method
    st.title("Software Developer Salary Prediction")
    st.write("""### We need some information to predict the salary""")


    countries = (
        "Australia",
        "Brazil",
        "Canada",
        "Denmark",
        "France",
        "Germany",
        "India",
        "Israel",
        "Italy",
        "Netherlands",
        "Norway",
        "Poland",
        "Spain",
        "Sweden",
        "Switzerland",
        "United Kingdom of Great Britain and Northern Ireland",
        "United States of America",
    )


    education  = (
        'Less than a Bachelors',
        'Bachelor’s degree',
        'Master’s degree',
        'Post grad'
    )

    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education)

    experience = st.slider("Years of Experience", 0, 50, 3)

    if ok := st.button("Calculate Salary"):
        X = np.array([[country, education, experience ]])
        X[:, 0] = le_country.transform(X[:, 0])
        X[:, 1] = le_education.transform(X[:, 1])
        X = X.astype(float)

        salary = regressor.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]:,.2f}")

    
    st_lottie(lottie_ML, speed=1, height=200, key="initial")
