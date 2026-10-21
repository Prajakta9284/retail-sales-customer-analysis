import pandas as pd 
import matplotlib.pyplot as plt 

# load dataset
df=pd.read_csv("retail_sales_transformed.csv")

print("Dataset shape: ",df.shape)

# customer revenue
customer_revenue=(
      df.groupby("Customer_ID")["Sales"]
      .sum()
      .sort_values(ascending=False)
)

print("\nTotal sales per customer: ")
print(customer_revenue.head(10))

# top customers
top_10_customers=customer_revenue.head(10)

print("\nTop 10 customers: ")
print(top_10_customers)

top_20_customers=customer_revenue.head(20)

print("\nTop 20 customers: ")
print(top_20_customers)

# average customer spending
total_customer_sales=customer_revenue.sum()

number_of_customers=df["Customer_ID"].nunique()

average_customer_spending=(
      total_customer_sales/number_of_customers
)

print("Total customer sales: ",round(total_customer_sales,2))
print("Number of customers: ",number_of_customers)
print(
      "Average customer spending: ",
      round(average_customer_spending)
)

# repeat customers
customer_orders=(
      df.groupby("Customer_ID")["Order_ID"]
      .nunique()
)

repeat_customers=customer_orders[
      customer_orders>1
]

one_time_customers=customer_orders[
      customer_orders==1
]

print("Repeat customers: ",len(repeat_customers))
print("One-time customers: ",len(one_time_customers))

print("\nRepeat customer ID: ")
print(repeat_customers)

# customer contribution
customer_contribution=(
      customer_revenue/total_customer_sales
) * 100

customer_contribution=customer_contribution.round(2)

print("\nCustomer revenue contribution: ")
print(customer_contribution.head(10))

# customer segement
customer_segment=pd.qcut(
      customer_revenue,
      q=3,
      labels=[
            "Low value",
            "Medium value",
            "High value"
      ]
)

customer_segment_data=pd.DataFrame({
      "Customer_ID": customer_revenue.index,
      "Total_Sales": customer_revenue.values,
      "Customer_Segment": customer_segment.values
})

print("\nCustomer segement: ")
print(customer_segment_data.head(10))

print("\nSegment distribution: ")
print(
      customer_segment_data[
            "Customer_Segment"
      ].value_counts()
)

df=df.merge(
      customer_segment_data[
            ["Customer_ID","Customer_Segment"]
      ],
      on="Customer_ID",
      how="left"
)

# visualizations
plt.figure(figsize=(10,6))

top_10_customers.sort_values().plot(
      kind="barh"
)

plt.title("Top 10 customers by revenue")
plt.xlabel("Sales")
plt.ylabel("Customer ID")

plt.tight_layout()
plt.show()

top_10_customers=(
      customer_contribution.head(10)
      .sort_values()
)

plt.figure(figsize=(10,6))

top_10_customers.plot(
      kind="barh"
)

plt.title("Top 10 customer revenue contribution")
plt.xlabel("Contribution (%)")
plt.ylabel("Customer ID")

plt.tight_layout()
plt.show()

segment_counts=(
      customer_segment_data[
            "Customer_Segment"
      ].value_counts()
)

plt.figure(figsize=(7,5))

segment_counts.plot(
      kind="barh"
)

plt.title("Customer segment distribution")
plt.xlabel("Customer segment")
plt.ylabel("Number of customers")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

repeat_data=pd.Series({
      "Repeat Customers": len(repeat_customers),
      "One_Time Cutomers": len(one_time_customers)
})

plt.figure(figsize=(7,5))

repeat_data.plot(
      kind="bar"
)

plt.title("Repeat vs One-Time customers")
plt.xlabel("Cuttomer type")
plt.ylabel("Number of customers")

plt.xticks(rotation=0)

plt.tight_layout()
plt.show()

print("---Customer Analysis Completed---")
print("Total customers: ",number_of_customers)
print("Average customer spending: ",round(average_customer_spending,2))
print("Repeat customers: ",len(repeat_customers))
print("One-Time customers: ",len(one_time_customers))
print("Top customers: ",customer_revenue.idxmax())
print("Top customer revenue: ",round(customer_revenue.max(),2))

print("\nCustomer analysis completed successfully!")
