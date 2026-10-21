import pandas as pd

# load dataset
df=pd.read_csv("retail_sales_transformed.csv")

df["Order_Date"]=pd.to_datetime(
      df["Order_Date"],
      dayfirst=True,
      errors="coerce"
)

for col in ["Sales","Profit","Quantity"]:
      df[col]=pd.to_numeric(df[col],errors="coerce")
      
df=df.dropna(
      subset=["Product","Order_Date","Sales","Profit"]
)

print("Dataset shape: ",df.shape)

output_columns=[
      "Analysis",
      "Product",
      "Category",
      "Total_Sales",
      "Total_Profit",
      "Total_Orders",
      "Total_Quantity",
      "Profit_Margin",
      "Monthly_Sales_Trend"
]

results=[]

# create product performance summary
product_summary=(
      df.groupby("Product")
      .agg(
            Category=("Category","first"),
            Total_Sales=("Sales","sum"),
            Total_Profit=("Profit","sum"),
            Total_Orders=("Order_ID","nunique"),
            Total_Quantity=("Quantity","sum")
            
      )
      .reset_index()
)

# calculate profit margin
product_summary["Profit_Margin"]=(
      product_summary["Total_Profit"]
      .div(
            product_summary["Total_Sales"].replace(0,float("nan"))
      )
      * 100
).round(2)

# add product results
def add_product_results(analysis_name,data):
      for _, row in data.iterrows():
            results.append({
                  "Analysis": analysis_name,
                  "Product": row["Product"],
                  "Category": row["Category"],
                  "Total_Sales": round(row["Total_Sales"],2),
                  "Total_Profit": round(row["Total_Profit"],2),
                  "Total_Orders": row["Total_Orders"],
                  "Total_Quantity": row["Total_Quantity"],
                  "Total_Margin": row["Profit_Margin"],
                  "Monthly_Sales_Trend": ""
            })
            
# top 10 products by sales
print("---Top 10 products---")

top_10=product_summary.sort_values(
      "Total_Sales", ascending=False
).head(10)

print(top_10.to_string(index=False))

add_product_results("Top 10 products",top_10)

# bottom 10 products by sales
print("---Bottom 10 products---")

bottom_10=product_summary.sort_values(
      "Total_Sales", ascending=True
).head(10)

print(bottom_10.to_string(index=False))

add_product_results("Bottom 10 products",bottom_10)

# most profitable products
print("---Most profitable products---")

most_profitable=product_summary.sort_values(
      "Total_Profit", ascending=False
).head(10)

print(most_profitable.to_string(index=False))

add_product_results("Most profitable products",most_profitable)

# high sales + low profit margin
print("---Low-Margin products---")

# Define high sales as above or equal to median product sales.
# Define low margin as below the median product profit margin

sales_threshold = product_summary["Total_Sales"].median()
margin_threshold = product_summary["Profit_Margin"].median()

low_margin = product_summary[
    (product_summary["Total_Sales"] >= sales_threshold)
    & (product_summary["Profit_Margin"] < margin_threshold)
].sort_values("Total_Sales", ascending=False)

print("High Sales Threshold:", round(sales_threshold, 2))
print("Low Margin Threshold:", round(margin_threshold, 2))
print("\nProducts with High Sales and Low Profit Margin:")

if low_margin.empty:
    print("No products match both conditions.")
else:
    print(low_margin.to_string(index=False))

add_product_results("High Sales Low Margin", low_margin)

# declining products
print("---Declining products---")

df["Year_Month"]=df["Order_Date"].dt.to_period("M")

monthly_product_sales=df.pivot_table(
      index="Product",
      columns="Year_Month",
      values="Sales",
      aggfunc="sum",
      fill_value=0
).sort_index(axis=1)

declining_products=[]

if monthly_product_sales.shape[1] < 3:
      print("Not enough monthly data to identify consistent declines.")
else:
      for product,sales in monthly_product_sales.iterrows():
            
            differences=sales.diff().dropna()
            
            if (differences<0).all():
                  trend = "->".join(
                        f"{month}: {value:.2f}"
                        for month, value in sales.items()
                  )
                  
                  declining_products.append({
                        "Product": product,
                        "Monthly_Sales_Trend": trend
                  })
                  
      if declining_products:
            declining_df=pd.DataFrame(declining_products)
            
            print(declining_df.to_string(index=False))
            
            for _, row in declining_df.iterrows():
                  product_row=product_summary[
                        product_summary["Product"]==row["Product"]
                  ].iloc[0]
                  
                  results.append({
                        "Analysis": "Declining products",
                        "Product": row["Product"],
                        "Category": product_row["Category"],
                        "Total_Sales": round(product_row["Total_Sales"],2),
                        "Total_Profit": round(product_row["Total_Profit"],2),
                        "Total_Orders": product_row["Total_Orders"],
                        "Total_Quantity": product_row["Total_Quantity"],
                        "Total_Margin": product_row["Total_Margin"],
                        "Monthly_Sales_Trend": row["Monthly_Sales_Trend"] 
                  })
                  
      else:
            print("No products show a decrease in every consecutive month.")
            
# category performance
print("---Category performance---")

category_summary=(
      df.groupby("Category")
      .agg(
            Total_Sales=("Sales","sum"),
            Total_Profit=("Profit","sum"),
            Total_Orders=("Order_ID","nunique"),
            Total_Quantity=("Quantity","sum")
      )
      .reset_index()
)

category_summary["Profit_Margin"]=(
      category_summary["Total_Profit"]
      .div(
            category_summary["Total_Sales"].replace(0,float("nan"))
      )
      * 100
).round(2)

category_summary=category_summary.sort_values(
      "Total_Sales", ascending=False
)

print(category_summary.to_string(index=False))

for _, row in category_summary.iterrows():
      results.append({
            "Analysis": "Category Performance",
            "Product": "",
            "Category": row["Category"],
            "Total_Sales": round(row["Total_Sales"], 2),
            "Total_Profit": round(row["Total_Profit"], 2),
            "Total_Orders": row["Total_Orders"],
            "Total_Quantity": row["Total_Quantity"],
            "Profit_Margin": row["Profit_Margin"],
            "Monthly_Sales_Trend": ""
      })
      
performance_df=pd.DataFrame(
      results,
      columns=output_columns
)

performance_df.to_csv(
      "product_performance.csv",
      index=False
)

print("\n---------------------------------------")
print("Product analysis completed successfully")
print("---------------------------------------")

print("Output file: product_performance_csv")
print("Total result rows:", len(performance_df))
print("\nAnalysis sections:")
print(performance_df["Analysis"].value_counts().to_string())