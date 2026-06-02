import requests
import streamlit as st


API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="OTA Validation Dashboard",
    layout="wide"
)

st.title("OTA Validation & Monitoring Dashboard")


def get_api_data(endpoint):
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=5)
        return response.json()
    except Exception as error:
        return {"error": str(error)}


vehicles = get_api_data("/vehicles")
campaigns = get_api_data("/campaigns")

st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Select View",
    [
        "Overview",
        "Vehicles",
        "Campaigns",
        "OTA Status",
        "Release KPI View"
    ]
)


if page == "Overview":
    st.header("System Overview")

    vehicle_count = len(vehicles) if isinstance(vehicles, list) else 0
    campaign_count = len(campaigns) if isinstance(campaigns, list) else 0

    active_campaigns = 0
    fota_campaigns = 0
    aota_campaigns = 0

    if isinstance(campaigns, list):
        active_campaigns = len([c for c in campaigns if c.get("status") == "ACTIVE"])
        fota_campaigns = len([c for c in campaigns if c.get("update_type") == "FOTA"])
        aota_campaigns = len([c for c in campaigns if c.get("update_type") == "AOTA"])

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Vehicles", vehicle_count)
    col2.metric("Campaigns", campaign_count)
    col3.metric("Active Campaigns", active_campaigns)
    col4.metric("Backend", "Online")

    st.subheader("Campaign Type Summary")

    col5, col6 = st.columns(2)
    col5.metric("FOTA Campaigns", fota_campaigns)
    col6.metric("AOTA Campaigns", aota_campaigns)

    st.info(
        "This dashboard monitors OTA campaign targeting, vehicle inventory, "
        "OTA status, and release-level KPIs."
    )


elif page == "Vehicles":
    st.header("Vehicle Inventory")

    if isinstance(vehicles, list):
        models = sorted(set(v.get("model", "") for v in vehicles))
        regions = sorted(set(v.get("region", "") for v in vehicles))
        update_types = sorted(set(v.get("update_type", "") for v in vehicles))

        col1, col2, col3 = st.columns(3)

        selected_model = col1.selectbox("Filter by Model", ["All"] + models)
        selected_region = col2.selectbox("Filter by Region", ["All"] + regions)
        selected_type = col3.selectbox("Filter by Update Type", ["All"] + update_types)

        filtered = vehicles

        if selected_model != "All":
            filtered = [v for v in filtered if v.get("model") == selected_model]

        if selected_region != "All":
            filtered = [v for v in filtered if v.get("region") == selected_region]

        if selected_type != "All":
            filtered = [v for v in filtered if v.get("update_type") == selected_type]

        st.dataframe(filtered, use_container_width=True)

    else:
        st.error(vehicles)


elif page == "Campaigns":
    st.header("OTA Campaigns")

    if isinstance(campaigns, list):
        statuses = sorted(set(c.get("status", "") for c in campaigns))
        priorities = sorted(set(c.get("priority", "") for c in campaigns))
        update_types = sorted(set(c.get("update_type", "") for c in campaigns))

        col1, col2, col3 = st.columns(3)

        selected_status = col1.selectbox("Filter by Status", ["All"] + statuses)
        selected_priority = col2.selectbox("Filter by Priority", ["All"] + priorities)
        selected_type = col3.selectbox("Filter by Update Type", ["All"] + update_types)

        filtered = campaigns

        if selected_status != "All":
            filtered = [c for c in filtered if c.get("status") == selected_status]

        if selected_priority != "All":
            filtered = [c for c in filtered if c.get("priority") == selected_priority]

        if selected_type != "All":
            filtered = [c for c in filtered if c.get("update_type") == selected_type]

        st.dataframe(filtered, use_container_width=True)

    else:
        st.error(campaigns)


elif page == "OTA Status":
    st.header("OTA Status Lookup")

    vin = st.text_input("Enter VIN", "VIN001")

    if st.button("Get OTA Status"):
        status = get_api_data(f"/ota/status/{vin}")

        if "error" in status:
            st.error(status)
        else:
            col1, col2, col3 = st.columns(3)

            col1.metric("VIN", status.get("vin", "N/A"))
            col2.metric("State", status.get("state", "N/A"))
            col3.metric("Progress", f"{status.get('progress', 0)}%")

            st.subheader("Full OTA Status Payload")
            st.json(status)


elif page == "Release KPI View":
    st.header("Release KPI View")

    st.write("Feature Owner / Product Owner style campaign health summary.")

    total_vehicles = len(vehicles) if isinstance(vehicles, list) else 0
    total_campaigns = len(campaigns) if isinstance(campaigns, list) else 0

    blocked_security = 0
    blocked_battery = 0

    if isinstance(vehicles, list):
        blocked_security = len(
            [
                v for v in vehicles
                if not v.get("package_signature_valid", True)
                or not v.get("checksum_valid", True)
                or not v.get("certificate_valid", True)
                or not v.get("tls_enabled", True)
            ]
        )

        blocked_battery = len(
            [
                v for v in vehicles
                if v.get("battery", 100) < 60
            ]
        )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Vehicles", total_vehicles)
    col2.metric("Total Campaigns", total_campaigns)
    col3.metric("Battery Risk Vehicles", blocked_battery)
    col4.metric("Cybersecurity Risk Vehicles", blocked_security)

    st.subheader("Release Interpretation")

    st.write(
        "- Battery risk vehicles may require update deferral or retry scheduling.\n"
        "- Cybersecurity risk vehicles should be blocked from install until package validation passes.\n"
        "- Campaign health can be monitored through eligibility, safety, cybersecurity, and OTA state results."
    )