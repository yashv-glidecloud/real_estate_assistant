import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(
    page_title="Real Estate Assistant",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Real Estate Assistant")
st.caption("Type what you're looking for in natural language")

# -------------------------------------------------
# FORM (auto-clears input after submit)
# -------------------------------------------------
with st.form(key="search_form", clear_on_submit=True):
    user_message = st.text_input(
        "What kind of property are you looking for?",
        placeholder="e.g. Show me 2bhk flats in Hinjewadi, Pune under 80 lakhs"
    )

    search_clicked = st.form_submit_button("Search")

# -------------------------------------------------
# API Call
# -------------------------------------------------
if search_clicked and user_message.strip():
    with st.spinner("Searching properties..."):
        try:
            response = requests.post(
                API_URL,
                json={"message": user_message},
                timeout=30
            )

            if response.status_code != 200:
                st.error(f"API Error: {response.status_code}")
            else:
                data = response.json()

                # ---- Answer ----
                st.subheader("Assistant")
                st.write(data.get("answer", ""))

                # ---- Filters Used ----
                with st.expander("🔍 Filters understood by the system"):
                    st.json(data.get("filters_used", {}))

                results = data.get("results", [])

                # ---- Results ----
                st.subheader("🏘️ Properties")

                if not results:
                    st.info("No properties found.")
                else:
                    for prop in results:
                        with st.container(border=True):
                            st.markdown(
                                f"""
                                **Property:** {prop['property_name']} (`{prop['property_id']}`)  
                                **Location:** {prop['area']}, {prop['city']}  
                                **BHK:** {prop['bhk']}  
                                **Price:** ₹{prop['price_lakhs']} lakhs  

                                {prop['description']}
                                """
                            )

        except requests.exceptions.RequestException as e:
            st.error("Could not connect to backend API.")
            st.exception(e)
