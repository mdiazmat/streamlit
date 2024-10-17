import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on Oct 7th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")

# (1) Dropdown for Category selection
category_selected = st.selectbox("Select a Category", df['Category'].unique())

filtered_df = df[df['Category'] == category_selected]

# Part 2: Adding a Multi-Select for Sub-Category based on the selected Category
if not filtered_df.empty:
    if 'Sub-Category' in filtered_df.columns:
        sub_category_selected = st.multiselect("Select Sub-Category", filtered_df['Sub-Category'].unique())

        if sub_category_selected:
            filtered_df = filtered_df[filtered_df['Sub-Category'].isin(sub_category_selected)]

# Part 3: Show a Line Chart of Sales for the Selected Sub-Categories

# Convert 'Ship_Date' to datetime format (this is necessary for grouping by month)
filtered_df['Ship_Date'] = pd.to_datetime(filtered_df['Ship_Date'], errors='coerce')

# Set the 'Ship_Date' column as the index
filtered_df_with_date_index = filtered_df.set_index('Ship_Date')

# Group by the 'Ship_Date' using monthly frequency and sum the sales
sales_by_month_filtered = filtered_df_with_date_index.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

# Display the line chart of sales by month
st.line_chart(sales_by_month_filtered, y="Sales")

# Part 4: Show three metrics: total sales, total profit, and overall profit margin (%)

if not filtered_df.empty:
    # Calculate total sales
    total_sales = filtered_df['Sales'].sum()

    # Calculate total profit
    total_profit = filtered_df['Profit'].sum()

    # Calculate overall profit margin (%)
    if total_sales != 0:
        profit_margin = (total_profit / total_sales) * 100
    else:
        profit_margin = 0

    # Display the metrics using st.metric
    st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
    st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
    st.metric(label="Overall Profit Margin (%)", value=f"{profit_margin:.2f}%")
else:
    st.write("No data available for the selected sub-categories.")
# Part 5: Use the delta option in the overall profit margin metric

# Calculate the overall average profit margin across all categories (entire dataset)
total_sales_all = df['Sales'].sum()
total_profit_all = df['Profit'].sum()

if total_sales_all != 0:
    overall_profit_margin_all = (total_profit_all / total_sales_all) * 100
else:
    overall_profit_margin_all = 0

# Calculate the delta (difference) between selected sub-categories' profit margin and the overall average
delta_profit_margin = profit_margin - overall_profit_margin_all

# Display the overall profit margin with delta
st.metric(
    label="Overall Profit Margin (%)",
    value=f"{profit_margin:.2f}%",
    delta=f"{delta_profit_margin:.2f}%"
)
