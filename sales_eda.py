import pandas as pd
import matplotlib.pyplot as plt 

# load dataset
df=pd.read_csv("retail_sales_transformed.csv")

df["Order_Date"]=pd.to_datetime(
      df["Order_Date"],
      dayfirst=True,
      errors="coerce"
)

print("Dataset shape: ",df.shape)
print("\nColumns: ")
print(df.columns.to_list())

# total sales
total_sales=df["Sales"].sum()

print("Total sales: ",round(total_sales,2))

# monthly sales
df["Year_Month"]=df["Order_Date"].dt.to_period("M")

monthly_sales=(
      df.groupby("Year_Month")["Sales"]
      .sum()
      .reset_index()
)

print(monthly_sales)

plt.figure(figsize=(10,5))

plt.plot(
      monthly_sales["Year_Month"].astype(str),
      monthly_sales["Sales"],
      marker="o"
)

plt.title("Monthly sales")
plt.xlabel("Month")
plt.ylabel("Sales")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# category sales
category_sales=(
      df.groupby("Category")["Sales"]
      .sum()
      .sort_values(ascending=False)
)

print(category_sales)

plt.figure(figsize=(8,5))

category_sales.plot(kind="bar")

plt.title("Sales by category")
plt.xlabel("Category")
plt.ylabel("Sales")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# regional sales
region_sales=(
      df.groupby("Region")["Sales"]
      .sum()
      .sort_values(ascending=False)
)

print(region_sales)

plt.figure(figsize=(8,5))

region_sales.plot(kind="bar")

plt.title("Sales by region")
plt.xlabel("Region")
plt.ylabel("Sales")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# product sales
product_sales=(
      df.groupby("Product")["Sales"]
      .sum()
      .sort_values(ascending=False)
)

print("\nTop 10 product: ")
print(product_sales.head(10))

print("\nBottom 10 product: ")
print(product_sales.tail(10))

top_10_product=product_sales.head(10)

plt.figure(figsize=(10,6))

top_10_product.sort_values().plot(kind="barh")

plt.title("Top 10 product by sales")
plt.xlabel("Sales")
plt.ylabel("Product")

plt.tight_layout()
plt.show()

# profit analysis
total_profit=df["Profit"].sum()

print("\nTotal profit: ",round(total_profit,2))

profit_category=(
      df.groupby("Category")["Profit"]
      .sum()
      .sort_values(ascending=False)
)

print("\nProfit by category: ")
print(profit_category)

profit_region=(
      df.groupby("Region")["Profit"]
      .sum()
      .sort_values(ascending=False)
)

print("\nProfit by region: ")
print(profit_region)

profit_product=(
      df.groupby("Product")["Profit"]
      .sum()
      .sort_values(ascending=False)
)

print("\nProfit by product: ")
print(profit_product)

# profit visualization
plt.figure(figsize=(8,5))

profit_category.plot(kind="bar")

plt.title("Profit by category")
plt.xlabel("Category")
plt.ylabel("Profit")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

plt.figure(figsize=(8,5))

profit_region.plot(kind="bar")

plt.title("Profit by region")
plt.xlabel("Region")
plt.ylabel("Profit")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# sales distribution
plt.figure(figsize=(8,5))

plt.hist(
      df["Sales"].dropna(),
      bins=20
)

plt.title("Sales distribution")
plt.xlabel("Sales")
plt.ylabel("Frequency")

plt.tight_layout()
plt.show()

print("---Sales EDA---")

print("Total sales: ",round(total_sales,2))
print("Total profit: ",round(total_profit,2))

print("\nBest category: ")
print(category_sales.idxmax())

print("\nBest region: ")
print(region_sales.idxmax())

print("\nTop product: ")
print(product_sales.idxmax())

print("\nMost profitable category: ")
print(profit_category.idxmax())

print("\nMost profitable region: ")
print(profit_region.idxmax())


