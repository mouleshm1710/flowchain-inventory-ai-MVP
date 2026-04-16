import streamlit as st
import pandas as pd

st.set_page_config(page_title="FlowChain Inventory Risk Intelligence AI - MVP", layout="wide")

st.title("FlowChain Inventory Risk Intelligence AI - MVP")
st.write("Upload inventory data to identify stockout and overstock risks.")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df)

    required_cols = ["SKU", "Demand", "Inventory", "Lead Time"]

    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        st.error(f"Missing required columns: {missing_cols}")
    else:
        #avg_demand = df["Demand"].mean()

        df["Stockout Risk"] = df["Inventory"] < (df["Demand"] * df["Lead Time"])
        df["Overstock Risk"] = df["Inventory"] > (df["Demand"] * df["Lead Time"] * 2)

        def recommendation(row):
            if row["Stockout Risk"]:
                return "Review replenishment quantity or timing"
            if row["Overstock Risk"]:
                return "Reduce inventory exposure or investigate slow-moving demand"
            return "Inventory level appears normal"

        df["Recommendation"] = df.apply(recommendation, axis=1)

        st.subheader("Risk Analysis Results")
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

        st.subheader("Summary")
        st.write(f"Average Demand: {avg_demand:.2f}")
        st.write(f"Stockout Risk Count: {df['Stockout Risk'].sum()}")
        st.write(f"Overstock Risk Count: {df['Overstock Risk'].sum()}")
