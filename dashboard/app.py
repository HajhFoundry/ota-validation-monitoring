import requests
import streamlit as st


API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="OTA Validation Dashboard",
    layout="wide"
)

st.title("OTA Validation & Monitoring Dashboard")

st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Select View",
    [
        "Overview",
        "Vehicles",
        "Campaigns",
        "OTA Status"
    ]
)


def get_api_data(endpoint):
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}")
        return response.json()
    except Exception as error:
        return {"error": str(error)}


if page == "Overview":
    st.header("System Overview")

    st.write("Connected Vehicle OTA validation and monitoring platform.")

    col1, col2, col3 = st.columns(3)

    vehicles = get_api_data("/vehicles")
    campaigns = get_api_data("/campaigns")

    col1.metric("Vehicles", len(vehicles) if isinstance(vehicles, list) else 0)
    col2.metric("Campaigns", len(campaigns) if isinstance(campaigns, list) else 0)
    col3.metric("Backend", "Online")

elif page == "Vehicles":
    st.header("Vehicle Inventory")

    vehicles = get_api_data("/vehicles")

    if isinstance(vehicles, list):
        st.dataframe(vehicles, use_container_width=True)
    else:
        st.error(vehicles)

elif page == "Campaigns":
    st.header("OTA Campaigns")

    campaigns = get_api_data("/campaigns")

    if isinstance(campaigns, list):
        st.dataframe(campaigns, use_container_width=True)
    else:
        st.error(campaigns)

elif page == "OTA Status":
    st.header("OTA Status Lookup")

    vin = st.text_input("Enter VIN", "VIN001")

    if st.button("Get OTA Status"):
        status = get_api_data(f"/ota/status/{vin}")
        st.json(status)