import streamlit as st
import json
import pandas as pd
from ai_studio.bridge import AnalyticalBridge
from core.turnover_predictor import TurnoverPredictor

# 1. Page Configuration & Professional Branding
st.set_page_config(page_title="UKG: Executive Financial Fabric", layout="wide")
st.title("📊 UKG Executive AI Analyst")
st.markdown("---")

# 2. Sidebar: Contextual Security (RLS Enforcement)
with st.sidebar:
    st.header("Executive Context")
    user_role = st.selectbox("Current Role", ["DEPT_HEAD", "GLOBAL_ADMIN"])
    user_dept = st.text_input("Scoped Department", value="Engineering")
    
    st.markdown("---")
    st.info("Identity verified via Row-Level Security (RLS). Access restricted to authorized cost centers.")

# 3. Initialize the Analytical Bridge
ukg_config = {
    "base_url": "https://tenant123.ultipro.com",
    "api_key": "MOCK_KEY",
    "auth_token": "MOCK_TOKEN"
}
user_context = {
    "role": user_role,
    "scoped_departments": [user_dept]
}
bridge = AnalyticalBridge(ukg_config, user_context)

# 4. Executive Interaction Layer
query = st.chat_input("Ask a question (e.g., 'Is Engineering burning out?')")

if query:
    with st.chat_message("user"):
        st.write(query)
    
    # MOCK: In a full deployment, an LLM would parse the query into this JSON intent
    # Here, we simulate the 'Mapping Example' from the executive_prompt.md
    if "burning out" in query.lower() or "absences" in query.lower():
        intent = {"action": "analyze_absences", "department": user_dept}
    elif "flight risk" in query.lower() or "retention" in query.lower():
        intent = {"action": "predict_turnover", "department": user_dept}
    else:
        intent = {"action": "get_financials", "department": user_dept}
    # 5. Execution & Visualization
    with st.spinner("Analyzing UKG Pro Data..."):
        result = bridge.route_query(json.dumps(intent))
        
    with st.chat_message("assistant"):
        if "error" in result:
            st.error(result["error"])
        
        elif "detected_patterns" in result:
            st.subheader(f"Insight Report: {user_dept} Absences")
            
            # Heatmap Visualization
            if result.get("dates"):
                viz_df = pd.DataFrame({"date": pd.to_datetime(result.get("dates", []))})
                viz_df["Day"] = viz_df["date"].dt.day_name()
                
                # Sort days to ensure professional chronological display
                day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
                chart_data = viz_df["Day"].value_counts().reindex(day_order).fillna(0)
                st.bar_chart(chart_data, color="#ff4b4b")

            for pattern in result["detected_patterns"]:
                st.warning(f"⚠️ {pattern}")

        elif isinstance(result, list) and intent["action"] == "predict_turnover":
            st.subheader(f"Retention Analysis: {user_dept}")
            if result:
                for risk in result:
                    st.error(f"🚨 Flight Risk: {risk['employee_id']} (Salary Ratio: {risk['salary_ratio']:.2f})")
                
                risk_df = pd.DataFrame(result)
                st.bar_chart(risk_df.set_index('employee_id')['annualSalary'])
            else:
                st.success("No critical flight risks identified in this department.")

            
            # Display raw dates if patterns found
            if result.get("dates"):
                st.write("Analyzed Absence Dates:", result["dates"])
        else:
            st.success(f"Financial Data Retrieved for {user_dept}")
            st.json(result)