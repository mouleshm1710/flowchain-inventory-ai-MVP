import streamlit as st
import pandas as pd

st.set_page_config(page_title="FlowChain Inventory Risk Intelligence AI - MVP", layout="wide")

st.title("FlowChain Inventory Risk Intelligence AI - MVP")
st.markdown(
    "Analyze inventory data to identify **stockout** and **overstock** risks using a simple rule-based decision support workflow."
)
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

with col2:
    st.info(
        "Required columns: SKU, Demand, Inventory, Lead Time.\n\n"
        "Optional columns: Price, Promotion, Region, Category, Date."
    )

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Convert Date column if available
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])

    # adding "region" filter
    if "Region" in df.columns:
        selected_region = st.selectbox("Select Region", ["All"] + sorted(df["Region"].dropna().unique().tolist()))
        if selected_region != "All":
            df = df[df["Region"] == selected_region]

    # adding "category" filter
    if "Category" in df.columns:
        selected_category = st.selectbox("Select Category", ["All"] + sorted(df["Category"].dropna().unique().tolist()))
        if selected_category != "All":
            df = df[df["Category"] == selected_category]

    st.subheader("1. Dataset Preview")
    st.dataframe(df)

    required_cols = ["SKU", "Demand", "Inventory", "Lead Time"]
    missing_cols = [col for col in required_cols if col not in df.columns]

    st.markdown("---")
    st.subheader("2. Risk Analysis")
    st.markdown("Legend: 🔴 High Risk | 🟠 Medium Risk | ✅ Normal")

    if missing_cols:
        st.error(f"Missing required columns: {missing_cols}")
    else:
        df["Stockout Risk"] = df["Inventory"] < (df["Demand"] * df["Lead Time"])
        df["Overstock Risk"] = df["Inventory"] > (df["Demand"] * df["Lead Time"] * 2)

        def recommendation(row):
            if row["Stockout Risk"]:
                return "🔴 Review replenishment quantity or timing"
            if row["Overstock Risk"]:
                return "🟠 Reduce inventory exposure or investigate slow-moving demand"
            return "✅ Inventory level appears normal"

        df["Recommendation"] = df.apply(recommendation, axis=1)

        st.dataframe(
            df[
                [
                    "SKU",
                    "Demand",
                    "Inventory",
                    "Lead Time",
                    "Stockout Risk",
                    "Overstock Risk",
                    "Recommendation",
                ]
            ]
        )

    # code for visualization/charts
        st.markdown("---")
        st.subheader("3. Visual Insights")

        #col1 = st.columns(1)

        #with col1:
        st.markdown("#### Demand vs Inventory by SKU")
        chart_data = df.groupby("SKU")[["Demand", "Inventory"]].mean()
        st.bar_chart(chart_data)

        # with col2:
        #     st.markdown("#### Risk Distribution")
        #     risk_counts = pd.DataFrame(
        #         {
        #             "Risk Type": ["Stockout Risk", "Overstock Risk"],
        #             "Count": [df["Stockout Risk"].sum(), df["Overstock Risk"].sum()],
        #         }
        #     )
        #     st.bar_chart(risk_counts.set_index("Risk Type"))

        st.markdown("---")
        st.subheader("4. Summary Insights")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Stockout Risk Count", int(df["Stockout Risk"].sum()))

        with col2:
            st.metric("Overstock Risk Count", int(df["Overstock Risk"].sum()))

         # -------------------------------
        # Phase 2: Demand Trend Analysis
        # -------------------------------
        if "Date" in df.columns:
            st.markdown("---")
            st.subheader("5. Demand Trend Analysis")

            sku_options = sorted(df["SKU"].dropna().unique().tolist())
            selected_sku = st.selectbox("Select SKU for Trend Analysis", sku_options)

            sku_df = df[df["SKU"] == selected_sku].copy()
            sku_df = sku_df.sort_values("Date")

            if len(sku_df) >= 3:
                sku_df["Moving Average (3)"] = sku_df["Demand"].rolling(window=3).mean().astype(int)

                latest_demand = sku_df["Demand"].iloc[-1]
                latest_ma = sku_df["Moving Average (3)"].iloc[-1]

                if pd.isna(latest_ma):
                    trend_label = "Insufficient data"
                elif latest_demand > latest_ma:
                    trend_label = "Increasing Trend"
                elif latest_demand < latest_ma:
                    trend_label = "Declining Trend"
                else:
                    trend_label = "Stable Trend"

                st.markdown(f"**Trend Classification:** {trend_label}")

                trend_chart = sku_df.set_index("Date")[["Demand", "Moving Average (3)"]]
                st.line_chart(trend_chart)
                
                st.markdown("#### Trend Analysis Table")
                st.dataframe(
                    sku_df[
                        [
                            "SKU",
                            "Date",
                            "Demand",
                            "Moving Average (3)",
                        ]
                    ]
                )
            else:
                st.warning("At least 3 time periods are required for trend analysis.")
