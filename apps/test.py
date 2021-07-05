import json
import folium
import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_folium import folium_static

# import numpy as np


cases = pd.read_csv("https://api.covid19india.org/csv/latest/state_wise.csv")
jeojson_file = json.load(open("apps\maps\states_india.geojson"))

new_cases = cases.drop([0, 31])

state_id_map = {}
for feature in jeojson_file["features"]:
    feature["id"] = feature["properties"]["state_code"]
    state_id_map[feature["properties"]["st_nm"]] = feature["id"]

state_id_map["Andaman and Nicobar Islands"] = state_id_map.pop(
    "Andaman & Nicobar Island"
)
state_id_map["Arunachal Pradesh"] = state_id_map.pop("Arunanchal Pradesh")
state_id_map["Dadra and Nagar Haveli and Daman and Diu"] = state_id_map.pop(
    "Dadara & Nagar Havelli"
)
state_id_map["Dadra and Nagar Haveli and Daman and Diu"] = state_id_map.pop(
    "Daman & Diu"
)
state_id_map["Delhi"] = state_id_map.pop("NCT of Delhi")
state_id_map["Jammu and Kashmir"] = state_id_map.pop("Jammu & Kashmir")
state_id_map["Ladakh"] = 1

new_cases["id"] = new_cases["State"].apply(lambda x: state_id_map[x])


st.set_page_config(layout="wide")


st.title("COVID-19 Cases in India")
st.info("This is usually pretty updated but it depends on MoHFW")
st.markdown("The dashboard will visualize the Covid-19 Situation in India")
st.markdown(
    "Coronavirus disease (COVID-19) is an infectious disease caused by a newly discovered coronavirus. \
    Most people infected with the COVID-19 virus will experience mild to moderate respiratory illness and recover without requiring special treatment."
)
choice = ["Confirmed", "Active", "Recovered", "Deaths"]
choice_selected = st.selectbox("Select Choice ", choice)

left, right = st.beta_columns(2)

with left:
    m = folium.Map(
        location=[23.47, 77.94],
        tiles="CartoDB positron",
        name="Map",
        zoom_start=5,
        attr="My Data Attribution",
        max_bounds=True,
    )

    chloropleth = folium.Choropleth(
        geo_data=jeojson_file,
        name="choropleth",
        data=new_cases,
        columns=["id", choice_selected],
        key_on="feature.properties.state_code",
        fill_color="Spectral",
        fill_opacity=0.7,
        line_opacity=0.3,
        legend_name=choice_selected + " Cases",
    ).add_to(m)

    folium.features.GeoJson(
        "states_india.geojson",
        name="LSOA Code",
        popup=folium.features.GeoJsonPopup(
            fields=["st_nm", "state_code"], alias=["State"]
        ),
    ).add_to(m)

    folium_static(m, width=1000, height=1000)

with right:
    st.dataframe(new_cases[["State", choice_selected]], height=500)
    # log_chart = st.checkbox("Show the charts in a logarithmic scale")
    # if log_chart:
    #     st.bar_chart(np.log(new_cases[choice]))
    # else:
    #     st.bar_chart(new_cases[choice])

    fig = px.histogram(
        new_cases,
        x="State",
        y=choice_selected,
        marginal="box",
    )
    st.plotly_chart(fig, use_container_width=True)
