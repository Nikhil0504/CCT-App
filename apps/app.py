import datetime
import json
import numpy as np
import requests
import pandas as pd
import streamlit as st
from copy import deepcopy
from fake_useragent import UserAgent


st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="https://www.cowin.gov.in/favicon.ico",
    page_title="CoWIN Vaccination Slot Availability",
)


@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def load_mapping():
    return pd.read_csv("apps\district_mapping.csv")


def filter_column(df, col, value):
    return deepcopy(df.loc[df[col] == value, :])


def filter_capacity(df, col, value):
    return deepcopy(df.loc[df[col] > value, :])


@st.cache(allow_output_mutation=True)
def Pageviews():
    return []


mapping_df = load_mapping()

rename_mapping = {
    "date": "Date",
    "min_age_limit": "Minimum Age Limit",
    "available_capacity": "Available Capacity",
    "vaccine": "Vaccine",
    "pincode": "Pincode",
    "name": "Hospital Name",
    "state_name": "State",
    "district_name": "District",
    "block_name": "Block Name",
    "fee_type": "Fees",
}

st.title("CoWIN Vaccination Slot Availability")
st.info(
    "The CoWIN APIs are geo-fenced so sometimes you may not see an output! Please try after sometime "
)

valid_states = list(np.unique(mapping_df["state_name"].values))

left_column_1, center_column_1, right_column_1 = st.beta_columns(3)
with left_column_1:
    numdays = st.slider("Select Date Range", 1, 100, 1)

with center_column_1:
    state_input = st.selectbox("Select State", ["Tamil Nadu"] + valid_states)
    if state_input != "":
        mapping_df = filter_column(mapping_df, "state_name", state_input)

mapping_dict = pd.Series(
    mapping_df["district id"].values, index=mapping_df["district name"].values
).to_dict()

unique_districts = list(mapping_df["district name"].unique())
unique_districts.sort()
with right_column_1:
    district_input = st.selectbox("Select District", unique_districts)

DIST_ID = mapping_dict[district_input]

base = datetime.datetime.today()
date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
date_str = [x.strftime("%d-%m-%Y") for x in date_list]


temp_user_agent = UserAgent()
browser_header = {"User-Agent": temp_user_agent.random}


final_df = None
for input_date in date_str:
    URL = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={DIST_ID}&date={input_date}"
    response = requests.get(URL, headers=browser_header)
    if (response.ok) and ("centers" in json.loads(response.text)):
        resp_json = json.loads(response.text)["centers"]
        if resp_json is not None:
            df = pd.DataFrame(resp_json)
            if len(df):
                df = df.explode("sessions")
                df["min_age_limit"] = df.sessions.apply(lambda x: x["min_age_limit"])
                df["vaccine"] = df.sessions.apply(lambda x: x["vaccine"])
                df["available_capacity"] = df.sessions.apply(
                    lambda x: x["available_capacity"]
                )
                df["date"] = df.sessions.apply(lambda x: x["date"])
                df = df[
                    [
                        "date",
                        "available_capacity",
                        "vaccine",
                        "min_age_limit",
                        "pincode",
                        "name",
                        "state_name",
                        "district_name",
                        "block_name",
                        "fee_type",
                    ]
                ]
                final_df = (
                    pd.concat([final_df, df]) if final_df is not None else deepcopy(df)
                )
        else:
            st.error("No rows in the data Extracted from the API")


if (final_df is not None) and (len(final_df)):
    final_df.drop_duplicates(inplace=True)
    final_df.rename(columns=rename_mapping, inplace=True)

    (
        left_column_2,
        center_column_2,
        right_column_2,
        right_column_2a,
        right_column_2b,
    ) = st.beta_columns(5)
    with left_column_2:
        valid_pincodes = list(np.unique(final_df["Pincode"].values))
        pincode_inp = st.selectbox("Select Pincode", [""] + valid_pincodes)
        if pincode_inp != "":
            final_df = filter_column(final_df, "Pincode", pincode_inp)

    with center_column_2:
        valid_age = [18, 45]
        age_inp = st.selectbox("Select Minimum Age", [""] + valid_age)
        if age_inp != "":
            final_df = filter_column(final_df, "Minimum Age Limit", age_inp)

    with right_column_2:
        valid_payments = ["Free", "Paid"]
        pay_inp = st.selectbox("Select Free or Paid", [""] + valid_payments)
        if pay_inp != "":
            final_df = filter_column(final_df, "Fees", pay_inp)

    with right_column_2a:
        valid_capacity = ["Available"]
        cap_inp = st.selectbox("Select Availablilty", [""] + valid_capacity)
        if cap_inp != "":
            final_df = filter_capacity(final_df, "Available Capacity", 0)

    with right_column_2b:
        valid_vaccines = ["COVISHIELD", "COVAXIN", "SPUTNIK V"]
        vaccine_inp = st.selectbox("Select Vaccine", [""] + valid_vaccines)
        if vaccine_inp != "":
            final_df = filter_column(final_df, "Vaccine", vaccine_inp)

    table = deepcopy(final_df)
    table.reset_index(inplace=True, drop=True)
    st.table(table)
else:
    st.error("Unable to fetch data currently, please try after sometime")
