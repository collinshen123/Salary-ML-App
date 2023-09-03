import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 

def shortened_categories(catagories, cutoff):
    catagorical_map = {}
    for i in range (len(catagories)):
        if catagories.values[i] >= cutoff:
            catagorical_map[catagories.index[i]] = catagories.index[i]
        else:
            catagorical_map[catagories.index[i]] = 'Other'
    return catagorical_map



def clean_experience(x):
    if x == 'Less than 1 year':
        return 0.5
    elif x == 'More than 50 years':
        return 51
    else:
        return float(x)




def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    elif 'Master’s degree' in x:
        return 'Master’s degree'
    elif 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    else:
        return 'Less than a Bachelors'
    

    

@st.cache_resource
def load_data():
    df = pd.read_parquet("survey_results_public.parquet")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    
    df = df[df["ConvertedCompYearly"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed, full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shortened_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[df["ConvertedCompYearly"] <= 250000]
    df = df[df["ConvertedCompYearly"] >= 10000]
    df = df[df["Country"] != "Other"]

    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write(
        """
    #### Data from Stack Overflow Developer Survey 2023
    """
    )
    st.write("")

    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", startangle=90)
    ax1.axis("equal")
    st.write("""#### Data from Different Countries""")
    st.pyplot(fig1)
    st.write("")

    st.write("""#### Average Salary Based on Country""")
    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)
    st.write("")

    st.write("""#### Average Salary Based on Experience""")
    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data, color="#000000")
    st.write("")

    st.write("""#### Average Salary Based on Education""")
    data = df.groupby(["EdLevel"])["Salary"].mean().sort_values(ascending=False)
    st.bar_chart(data, color="#8F00FF")