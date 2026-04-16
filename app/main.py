# import streamlit as st
# import pandas as pd

# st.set_page_config(page_title="FlowChain Inventory Risk Intelligence AI - MVP", layout="wide")

# st.title("FlowChain Inventory Risk Intelligence AI - MVP")
# st.write("Upload inventory data to identify stockout and overstock risks.")

# uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

# if uploaded_file is not None:
#     df = pd.read_csv(uploaded_file)

#     st.subheader("Preview of the dataset")
#     st.dataframe(df)

#     required_cols = ["SKU", "Demand", "Inventory", "Lead Time"]

#     missing_cols = [col for col in required_cols if col not in df.columns]

#     if missing_cols:
#         st.error(f"Missing required columns: {missing_cols}")
#     else:
#         #avg_demand = df["Demand"].mean()

#         df["Stockout Risk"] = df["Inventory"] < (df["Demand"] * df["Lead Time"])
#         df["Overstock Risk"] = df["Inventory"] > (df["Demand"] * df["Lead Time"] * 2)

#         def recommendation(row):
#             if row["Stockout Risk"]:
#                 return "Review replenishment quantity or timing"
#             if row["Overstock Risk"]:
#                 return "Reduce inventory exposure or investigate slow-moving demand"
#             return "Inventory level appears normal"

#         df["Recommendation"] = df.apply(recommendation, axis=1)

#         st.subheader("Risk Analysis Results")
#         st.dataframe(
#             df[
#                 [
#                     "SKU",
#                     "Demand",
#                     "Inventory",
#                     "Lead Time",
#                     "Stockout Risk",
#                     "Overstock Risk",
#                     "Recommendation",
#                 ]
#             ]
#         )

#         st.subheader("Summary")
#         #st.write(f"Average Demand: {avg_demand:.2f}")
#         st.write(f"Stockout Risk Count: {df['Stockout Risk'].sum()}")
#         st.write(f"Overstock Risk Count: {df['Overstock Risk'].sum()}")



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
        "Optional columns: Price, Promotion, Region, Category."
    )

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("1. Dataset Preview")
    st.dataframe(df)

    required_cols = ["SKU", "Demand", "Inventory", "Lead Time"]
    missing_cols = [col for col in required_cols if col not in df.columns]

    st.markdown("---")
    st.subheader("2. Risk Analysis")

    if missing_cols:
        st.error(f"Missing required columns: {missing_cols}")
    else:
        df["Stockout Risk"] = df["Inventory"] < (df["Demand"] * df["Lead Time"])
        df["Overstock Risk"] = df["Inventory"] > (df["Demand"] * df["Lead Time"] * 2)

        def recommendation(row):
            if row["Stockout Risk"]:
                return "Review replenishment quantity or timing"
            if row["Overstock Risk"]:
                return "Reduce inventory exposure or investigate slow-moving demand"
            return "Inventory level appears normal"

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

        st.markdown("---")
        st.subheader("3. Summary Insights")

        col1, col2 = #t.columns(2)

        with col1:
            st.metric("Stockout Risk Count", int(df["Stockout Risk"].sum()))

        with col2:
            st.metric("Overstock Risk Count", int(df["Overstock Risk"].sum()))
