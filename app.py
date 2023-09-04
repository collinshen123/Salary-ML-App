import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page

st.sidebar.selectbox("Explore or Predict", ("ML Prediction", "Explore Data"))


show_predict_page()
# if page == "Predict":
#     show_predict_page()
# else:
#     show_explore_page()
