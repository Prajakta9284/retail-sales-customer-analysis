import pandas as pd 

# load dataset
df=pd.read_csv("retail_sales_messy.csv")

print("Original shape: ",df.shape)

# handle missing values
print("\nMissing values before cleaning: ")
print(df.isnull().sum())

categorical_columns=[
      "Customer_Name",
      "Product",
      "Category",
      "Region",
      "Payment_Method"
]

for column in categorical_columns:
      df[column]=df[column].fillna("Unknown")
      
numeric_columns=[
      "Quantity",
      "Unit_Price",
      "Discount",
      "Sales",
      "Cost",
      "Profit",
]

for column in numeric_columns:
      df[column]=df[column].fillna(df[column].median())
      
# remove duplicates
print("\nDuplicate records: ",df.duplicated().sum())

df=df.drop_duplicates()

# fix data types
df["Order_Date"]=pd.to_datetime(
      df["Order_Date"],
      errors="coerce"
)

for column in numeric_columns:
      df[column]=pd.to_numeric(
            df[column],
            errors="coerce"
      )
df["Quantity"]=df["Quantity"].astype("Int64")

# check invalid sales
invalid_sales=df[
      (df["Sales"]<0) |
      (df["Sales"]==0)
]

print("\nInvalid sales records: ")
print(invalid_sales)

df=df[df["Sales"]>=0]

# standardize categories
df["Category"]=df["Category"].str.strip()
df["Category"]=df["Category"].str.title()

print("\nCategories after cleaning: ")
print(df["Category"].unique())

# validate dates
print("\nInvalid dates: ",df["Order_Date"].isna().sum())

df=df.dropna(subset=["Order_Date"])

today=pd.Timestamp.today()

future_dates=df[df["Order_Date"]>today]

print("Future date records: ",len(future_dates))

print("\nFinal shape: ",df.shape)

print("\nMissing values after cleaning: ")
print(df.isnull().sum())

print("\nData types: ")
print(df.dtypes)

df.to_csv("retail_sales_cleaned.csv", index=False)

print("\nCleaned dataset saved successfully!")