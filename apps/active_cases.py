import streamlit as st
import pandas as pd
import requests, json


st.title("COVID-19 Cases in India")
st.info("This is usually pretty updated but it depends on MoHFW")
st.markdown("The dashboard will visualize the Covid-19 Situation in India")
st.markdown(
    "Coronavirus disease (COVID-19) is an infectious disease caused by a newly discovered coronavirus. \
    Most people infected with the COVID-19 virus will experience mild to moderate respiratory illness and recover without requiring special treatment."
)
# st.sidebar.title("Visualization Selector")
# st.sidebar.markdown("Select the Charts/Plots accordingly:")

a = requests.get(
    "https://api.apify.com/v2/key-value-stores/toDWvRj1JpTXiM8FF/records/LATEST?disableRedirect=true.json"
)
b = pd.DataFrame(json.loads(a.text)["regionData"])


rename_mapping = {
    "region": "Region",
    "activeCases": "Active Cases",
    "newInfected": "New Infected Cases",
    "recovered": "Recovered Cases",
    "newRecovered": "New Recovered Cases",
    "deceased": "Deceased Cases",
    "newDeceased": "Recently Deceased Cases",
    "totalInfected": "Total Infected Cases",
}
b.rename(columns=rename_mapping, inplace=True)

select = st.sidebar.selectbox(
    "Cases type",
    ["", "Active Cases", "Recovered Cases", "Deceased Cases", "Total Infected Cases"],
    key="3",
)


def table(b):
    T = st.write(
        "These are the states that are currently being moniored:",
        b["Region"],
        "The numbers on the left side will help you locate the state you want to check.",
    )
    return T


# st.table(b)
# st.bar_chart(b["Active Cases"])
# st.bar_chart(b["Recovered Cases"])
# st.bar_chart(b["Deceased Cases"])
# st.bar_chart(b["Total Infected Cases"])

if select == "":
    st.table(b)
if select == "Active Cases":
    table(b)
    st.bar_chart(b["Active Cases"])
if select == "Recovered Cases":
    table(b)
    st.bar_chart(b["Recovered Cases"])
if select == "Deceased Cases":
    table(b)
    st.bar_chart(b["Deceased Cases"])
if select == "Total Infected Cases":
    table(b)
    st.bar_chart(b["Total Infected Cases"])
