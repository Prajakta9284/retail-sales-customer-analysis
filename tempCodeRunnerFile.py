df=pd.read_csv("retail_sales_cleaned.csv")

# df["Profit_Margin"]=0

# df.loc[df["Sales"] != 0, "Profit_Magin"] = (
#       df.loc[df["Sales"] != 0, "Profit"]
#       / df.loc[df["Sales"] != 0, "Sales"]
# )

# df["Profit_Margin"]=df["Profit_Margin"].round(2)

# print(df[[
#       "Product",
#       "Sales",
#       "Profit",
#       "Profit_Margin"
# ]].head())

# df.to_csv("transformed_retail_sales.csv",index=False)

# print("Profit margin created successfully!")