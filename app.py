import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------
# PAGE CONFIG
# --------------------------------

st.set_page_config(
    page_title="ATM Cash Demand Prediction",
    page_icon="🏦",
    layout="wide"
)

# --------------------------------
# CUSTOM CSS
# --------------------------------

st.markdown("""
<style>

.main{
    background-color:#F5F7FA;
}

.block-container{
    padding-top:1rem;
    max-width:1400px;
}

.metric-container{
    background:white;
    padding:15px;
    border-radius:15px;
    border:1px solid #E5E7EB;
    box-shadow:0px 2px 8px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# HEADER
# --------------------------------

st.markdown("""
<div style="
background:linear-gradient(90deg,#0A2A66,#1565C0);
padding:25px;
border-radius:15px;
color:white;
text-align:center;
">

<h1>🏦 ATM Cash Demand Prediction System</h1>

<p style="font-size:18px;">
AI-Powered Cash Forecasting & Refill Recommendation
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# --------------------------------
# MAIN LAYOUT
# --------------------------------

left_col, right_col = st.columns([1, 2])

# --------------------------------
# INPUTS
# --------------------------------

with left_col:

    st.subheader("🏦 ATM & Event Details")

    total_withdrawals = st.number_input("Total Withdrawals")

    total_deposits = st.number_input("Total Deposits")

    previous_day_cash = st.number_input(
        "Previous Day Cash Level"
    )


    holiday_flag = st.selectbox(
        "Holiday",
        ["No","Yes"]
    )

    special_event = st.selectbox(
        "Special Event",
        ["No","Yes"]
    )

    day_of_week = st.selectbox(
        "Day",
        [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]
    )

    weather = st.selectbox(
        "Weather",
        [
            "Clear",
            "Cloudy",
            "Rainy"
        ]
    )
    

    
    

# --------------------------------
# CHART
# --------------------------------

with right_col:
    st.markdown("---")

    st.subheader("🏧 ATM Information")

    atm_number = st.text_input(
        "ATM Number",
        value="ATM-101"
    )

    atm_location = st.selectbox(
        "ATM Location",
        [
            "Mall",
            "Railway Station",
            "Airport",
            "Bank Branch",
            "Market Area",
            "IT Park"
        ]
    )

    nearby_competitor_atms = st.number_input(
        "Nearby Competitor ATMs",
        min_value=0,
        value=2
    )

    st.subheader("📊 Historical Demand")

    lag_1 = st.number_input(
        "Yesterday Demand"
    )

    lag_2 = st.number_input(
        "2 Days Ago Demand"
    )

    lag_3 = st.number_input(
        "3 Days Ago Demand"
    )

st.subheader("📈 Demand Trend")

trend_df = pd.DataFrame({
        "Day": [
            "3 Days Ago",
            "2 Days Ago",
            "Yesterday"
        ],
        "Demand": [
            lag_3,
            lag_2,
            lag_1
        ]
    })

fig = px.line(
        trend_df,
        x="Day",
        y="Demand",
        markers=True
    )

fig.update_layout(
        height=250,
        margin=dict(l=10, r=10, t=30, b=10)
    )

st.plotly_chart(
        fig,
        use_container_width=True
    )


# =====================================
# PREDICTION
# =====================================
predict_btn = st.button(
    "🔮 Predict Cash Demand",
    use_container_width=True
)
if predict_btn:

    # Base Demand from Historical Data
    base_prediction = (
        lag_1 +
        lag_2 +
        lag_3
    ) / 3

    # Location Impact
    location_multiplier = {
        "Bank Branch": 1.00,
        "Mall": 1.20,
        "Railway Station": 1.30,
        "Airport": 1.40,
        "Market Area": 1.25,
        "IT Park": 1.15
    }

    location_factor = location_multiplier[atm_location]

    # Competitor Impact
    competitor_factor = max(
        0.75,
        1 - (nearby_competitor_atms * 0.03)
    )

    # Final Prediction
    prediction = (
        base_prediction *
        location_factor *
        competitor_factor
    )

    # Holiday Impact
    if holiday_flag == "Yes":
        prediction *= 1.10

    # Special Event Impact
    if special_event == "Yes":
        prediction *= 1.15

    # Remaining Cash
    remaining_cash = (
        previous_day_cash -
        prediction
    )

    # Refill Amount
    refill_amount = max(
        0,
        100000 - remaining_cash
    )

    # Days Left
    days_left = round(max(
        0,
        remaining_cash / prediction
    ))
  

    # Status
    if remaining_cash >= 100000:
        atm_status = "SAFE"

    elif remaining_cash >= 50000:
        atm_status = "WARNING"

    else:
        atm_status = "CRITICAL"

    # =====================================
    # RESULTS
    # =====================================

    st.write("")
    st.subheader("📊 Prediction Results")

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.metric(
            "💰 Predicted Demand",
            f"₹ {prediction:,.0f}"
        )

    with k2:
        st.metric(
            "💵 Remaining Cash",
            f"₹ {remaining_cash:,.0f}"
        )

    with k3:
        st.metric(
            "📦 Refill Amount",
            f"₹ {refill_amount:,.0f}"
        )

    with k4:
        st.metric(
            "⏳ Days Left",
            f"{days_left:,.0f} days"
        )

    st.write("")

    # ATM Status

    if atm_status == "SAFE":
        st.success(
            "✅ ATM Status : SAFE"
        )

    elif atm_status == "WARNING":
        st.warning(
            "⚠️ ATM Status : WARNING"
        )

    else:
        st.error(
            "🚨 ATM Status : CRITICAL"
        )

    # =====================================
    # AI RECOMMENDATION
    # =====================================

    st.write("")

    st.info(f"""
### 🤖 AI Recommendation

Predicted Cash Demand: ₹ {prediction:,.0f}

Remaining Cash: ₹ {remaining_cash:,.0f}

Recommended Refill Amount: ₹ {refill_amount:,.0f}

ATM Location: {atm_location}

Nearby Competitor ATMs: {nearby_competitor_atms}

Status: {atm_status}
""")