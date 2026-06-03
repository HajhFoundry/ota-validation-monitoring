import json
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

def post_api_data(endpoint, payload=None):
    try:
        response = requests.post(
            f"{API_BASE_URL}{endpoint}",
            json=payload,
            timeout=5
        )
        return response.json()
    except Exception as error:
        return {"error": str(error)}


vehicles = get_api_data("/vehicles")
campaigns = get_api_data("/campaigns")

if "manual_test_results" not in st.session_state:
    st.session_state.manual_test_results = []


st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Select View",
    [
        "Overview",
        "Vehicles",
        "Campaigns",
        "OTA Status",
        "Release KPI View",
        "Manual OTA Test Console",
        "Live OTA Operations"
    ]
)


if page == "Overview":
    st.header("System Overview")

    vehicle_count = len(vehicles) if isinstance(vehicles, list) else 0
    campaign_count = len(campaigns) if isinstance(campaigns, list) else 0

    active_campaigns = len([c for c in campaigns if c.get("status") == "ACTIVE"]) if isinstance(campaigns, list) else 0
    fota_campaigns = len([c for c in campaigns if c.get("update_type") == "FOTA"]) if isinstance(campaigns, list) else 0
    aota_campaigns = len([c for c in campaigns if c.get("update_type") == "AOTA"]) if isinstance(campaigns, list) else 0

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
        "OTA status, manual validation testing, and release-level KPIs."
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

    manual_total = len(st.session_state.manual_test_results)
    manual_passed = len([t for t in st.session_state.manual_test_results if t["result"] == "PASS"])
    manual_failed = len([t for t in st.session_state.manual_test_results if t["result"] == "FAIL"])

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Vehicles", total_vehicles)
    col2.metric("Total Campaigns", total_campaigns)
    col3.metric("Battery Risk Vehicles", blocked_battery)
    col4.metric("Cybersecurity Risk Vehicles", blocked_security)

    st.subheader("Manual Validation KPIs")

    col5, col6, col7 = st.columns(3)
    col5.metric("Manual Tests Run", manual_total)
    col6.metric("Passed", manual_passed)
    col7.metric("Failed", manual_failed)

    st.subheader("Release Interpretation")

    st.write(
        "- Battery risk vehicles may require update deferral or retry scheduling.\n"
        "- Cybersecurity risk vehicles should be blocked from install until package validation passes.\n"
        "- Manual validation KPIs help feature owners track pass/fail behavior during campaign readiness testing."
    )


elif page == "Manual OTA Test Console":
    st.header("Manual OTA Test Console")

    st.write(
        "Change vehicle conditions and run OTA validation manually. "
        "This simulates real-world validation testing."
    )

    vin = st.selectbox("Select VIN", ["VIN001", "VIN002", "VIN003"])
    campaign_id = st.selectbox(
        "Select Campaign",
        ["FOTA_2026_001", "AOTA_2026_001", "FOTA_2026_002"]
    )

    col1, col2, col3 = st.columns(3)

    battery = col1.slider("Battery %", 0, 100, 75)
    ignition = col2.checkbox("Ignition ON")
    driving = col3.checkbox("Vehicle Driving")

    col4, col5, col6, col7 = st.columns(4)

    wifi_connected = col4.checkbox("WiFi Connected", value=True)
    tls_enabled = col5.checkbox("TLS Enabled", value=True)
    certificate_valid = col6.checkbox("Certificate Valid", value=True)
    package_signature_valid = col7.checkbox("Package Signature Valid", value=True)

    checksum_valid = st.checkbox("Checksum Valid", value=True)

    if st.button("Run OTA Validation"):
        logs = []

        logs.append(f"[INFO] Selected VIN: {vin}")
        logs.append(f"[INFO] Selected Campaign: {campaign_id}")

        result = "PASS"
        final_decision = "OTA ALLOWED"

        if battery < 60:
            logs.append(f"[FAIL] Battery too low: {battery}%")
            result = "FAIL"
            final_decision = "OTA BLOCKED - LOW BATTERY"
        else:
            logs.append(f"[PASS] Battery OK: {battery}%")

        if ignition:
            logs.append("[FAIL] Ignition is ON")
            result = "FAIL"
            final_decision = "OTA BLOCKED - IGNITION ON"
        else:
            logs.append("[PASS] Ignition OFF")

        if driving:
            logs.append("[FAIL] Vehicle is driving")
            result = "FAIL"
            final_decision = "OTA BLOCKED - VEHICLE DRIVING"
        else:
            logs.append("[PASS] Vehicle parked")

        if not wifi_connected:
            logs.append("[FAIL] WiFi not connected")
            result = "FAIL"
            final_decision = "OTA BLOCKED - WIFI NOT CONNECTED"
        else:
            logs.append("[PASS] WiFi connected")

        if not tls_enabled:
            logs.append("[FAIL] TLS not enabled")
            result = "FAIL"
            final_decision = "OTA BLOCKED - TLS FAILURE"
        else:
            logs.append("[PASS] TLS enabled")

        if not certificate_valid:
            logs.append("[FAIL] Certificate invalid")
            result = "FAIL"
            final_decision = "OTA BLOCKED - CERTIFICATE FAILURE"
        else:
            logs.append("[PASS] Certificate valid")

        if not package_signature_valid:
            logs.append("[FAIL] Package signature invalid")
            result = "FAIL"
            final_decision = "OTA BLOCKED - SIGNATURE FAILURE"
        else:
            logs.append("[PASS] Package signature valid")

        if not checksum_valid:
            logs.append("[FAIL] Checksum validation failed")
            result = "FAIL"
            final_decision = "OTA BLOCKED - CHECKSUM FAILURE"
        else:
            logs.append("[PASS] Checksum valid")

        test_result = {
            "vin": vin,
            "campaign_id": campaign_id,
            "result": result,
            "decision": final_decision,
            "battery": battery,
            "ignition": ignition,
            "driving": driving,
            "wifi_connected": wifi_connected,
            "tls_enabled": tls_enabled,
            "certificate_valid": certificate_valid,
            "package_signature_valid": package_signature_valid,
            "checksum_valid": checksum_valid,
            "logs": logs
        }

        st.session_state.manual_test_results.append(test_result)

        st.subheader("Validation Summary")

        col_a, col_b = st.columns(2)
        col_a.metric("Result", result)
        col_b.metric("Final Decision", final_decision)

        if result == "PASS":
            st.success(final_decision)
        else:
            st.error(final_decision)

        st.subheader("Validation Logs")

        for log in logs:
            st.write(log)

    st.subheader("Manual Test Session Summary")

    total_tests = len(st.session_state.manual_test_results)
    passed_tests = len([t for t in st.session_state.manual_test_results if t["result"] == "PASS"])
    failed_tests = len([t for t in st.session_state.manual_test_results if t["result"] == "FAIL"])

    col_x, col_y, col_z = st.columns(3)

    col_x.metric("Total Tests Run", total_tests)
    col_y.metric("Passed", passed_tests)
    col_z.metric("Failed", failed_tests)

    if st.session_state.manual_test_results:
        st.dataframe(st.session_state.manual_test_results, use_container_width=True)
    else:
        st.info("No manual tests have been run yet.")

    report_text = json.dumps(
        st.session_state.manual_test_results,
        indent=4
    )

    st.download_button(
        label="Download Test Report",
        data=report_text,
        file_name="manual_ota_test_report.txt",
        mime="text/plain"
    )

    if st.button("Reset Test Session"):
        st.session_state.manual_test_results = []
        st.rerun()

elif page == "Live OTA Operations":
    st.header("Live OTA Operations Center")

    st.write(
        "Simulate a live OTA campaign execution and monitor OTA progress, "
        "state transitions, and operational logs."
    )

    vin = st.selectbox("Select Vehicle", ["VIN001", "VIN002", "VIN003"])
    campaign_id = st.selectbox(
        "Select OTA Campaign",
        ["FOTA_2026_001", "AOTA_2026_001", "FOTA_2026_002"]
    )

    if "live_ota_logs" not in st.session_state:
        st.session_state.live_ota_logs = []

    if "live_ota_state" not in st.session_state:
        st.session_state.live_ota_state = "IDLE"

    if "live_ota_progress" not in st.session_state:
        st.session_state.live_ota_progress = 0

    if "live_ota_results" not in st.session_state:
        st.session_state.live_ota_results = []

    col1, col2, col3 = st.columns(3)

    col1.metric("VIN", vin)
    col2.metric("OTA State", st.session_state.live_ota_state)
    col3.metric("Progress", f"{st.session_state.live_ota_progress}%")

    progress_bar = st.progress(st.session_state.live_ota_progress)

    if st.button("Start Live OTA Simulation"):
        st.session_state.live_ota_logs = []
        post_api_data(
            "/ota/start",
            {
                "vin": vin,
                "campaign_id": campaign_id
            }
        )

        ota_steps = [
            ("PENDING", 0),
            ("DOWNLOADING", 25),
            ("DOWNLOADING", 50),
            ("PAUSED_LOW_BATTERY", 50),
            ("RESUMING", 50),
            ("DOWNLOADING", 75),
            ("DOWNLOADING", 100),
            ("VERIFYING", 100),
            ("INSTALLING", 100),
            ("REBOOTING", 100),
            ("SUCCESS", 100)
        ]

        for state, progress in ota_steps:
            st.session_state.live_ota_state = state
            st.session_state.live_ota_progress = progress

            log_message = (
                f"[OTA EVENT] VIN={vin} "
                f"Campaign={campaign_id} "
                f"State={state} "
                f"Progress={progress}%"
            )

            st.session_state.live_ota_logs.append(log_message)
            

            post_api_data(
                "/ota/update-status",
                {
                    "vin": vin,
                    "campaign_id": campaign_id,
                    "state": state,
                    "progress": progress,
                    "message": f"OTA state changed to {state}"
                }
            )

        st.session_state.live_ota_results.append(
            {
                "vin": vin,
                "campaign_id": campaign_id,
                "final_state": st.session_state.live_ota_state,
                "progress": st.session_state.live_ota_progress,
                "event_count": len(st.session_state.live_ota_logs),
                "logs": st.session_state.live_ota_logs
            }
        )

        st.rerun()

    st.subheader("Current OTA Status")

    col4, col5, col6 = st.columns(3)
    col4.metric("Vehicle", vin)
    col5.metric("State", st.session_state.live_ota_state)
    col6.metric("Progress", f"{st.session_state.live_ota_progress}%")

    st.progress(st.session_state.live_ota_progress)

    st.subheader("OTA Event Logs")

    if st.session_state.live_ota_logs:
        for log in st.session_state.live_ota_logs:
            st.write(log)
    else:
        st.info("No live OTA events yet.")

    if st.button("Reset Live OTA"):
        st.session_state.live_ota_state = "IDLE"
        st.session_state.live_ota_progress = 0
        st.session_state.live_ota_logs = []
        st.rerun()