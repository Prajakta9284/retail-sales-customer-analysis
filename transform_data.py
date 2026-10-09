import pandas as pd

# load cleaned dataset
df=pd.read_csv("retail_sales_cleaned.csv")

print("Original shape: ",df.shape)

# date features
df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    dayfirst=True,
    errors="coerce"
)

df["Year"]=df["Order_Date"].dt.year
df["Month"]=df["Order_Date"].dt.month
df["Month_Name"]=df["Order_Date"].dt.month_name()
df["Day"]=df["Order_Date"].dt.day
df["Day_Name"]=df["Order_Date"].dt.day_name()
df["Quarter"]=df["Order_Date"].dt.quarter

# profit margin
df["Profit_Margin"]=(
      df["Profit"].div(
            df["Sales"].replace(0, pd.NA)
      ) * 100
).round(2)

# order value
df["Order_Value"]=(
      df["Quantity"] * df["Unit_Price"]
).round(2)

# customer segmentation
customer_sales=df.groupby("Customer_ID")["Sales"].sum()

customer_segment=pd.qcut(
      customer_sales,
      q=3,
      labels=("Low Value","Medium Value","High Value")
)

customer_data=pd.DataFrame({
      "Customer_ID": customer_sales.index,
      "Total_Customer_Sales": customer_sales.values,
      "Customer_Segment": customer_segment.values
})

df=df.merge(
      customer_data[
            ["Customer_ID","Customer_Segment"]
      ],
      on="Customer_ID",
      how="left"
)

print("\nCustomer segment counts: ")
print(df["Customer_Segment"].value_counts())

# additional analytical columns
df["Total_Cost"]=(
      df["Quantity"] * df["Unit_Price"]
).round(2)

df["Discount_Amount"]=(
      df["Quantity"]*
      df["Unit_Price"]*
      df["Discount"]/100
).round(2)

df["Sales_Per_Unit"]=(
      df["Sales"].div(
            df["Quantity"].replace(0, pd.NA)
      )
).round(2)

print("\nFinal columns: ")
print(df.columns.to_list())

print("\nTransformed dataset: ")
print(df.head(10))

df.to_csv(
      "retail_sales_transformed.csv",
      index=False
)

print("\nTransformed dataset saved successfully!")
print("File: retail_sales_transformed.csv")