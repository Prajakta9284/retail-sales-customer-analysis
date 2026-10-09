# Task 1 — Load Dataset 
import pandas as pd 

df=pd.read_csv("retail_sales_messy.csv")

# Task 2 — Inspect Dataset 
print(df.head())

print(df.tail())

print("Shape: ",df.shape)

print("Columns: ",df.columns)

print(df.dtypes)

print(df.info())

print(df.describe())

# Task 3 — Analyze Each Column 
for column in df.columns:
      print("\nColumn: ",column)
      print("Data type: ",df[column].dtypes)
      print("Missing values: ",df[column].isnull().sum())
      print("Unique values: ",df[column].nunique())
      
for column in df.columns:
      print("\n---", column, "---")
      print(df[column].unique()[:20])

print("Duplicate rows: ",df.duplicated().sum())
      
print(df.isnull().sum())

# Task 4 — Analyze Unique Values
for column in df.columns:
      print(column, ":", df[column].nunique())
      
for column in df.columns:
      print("\n", column)
      print(df[column].unique()[:20])
      
print("Categories: ")
print(df["Category"].value_counts())

print("\nRegions: ")
print(df["Region"].value_counts())   

print("Unique customers: ",df["Customer_ID"].nunique())   
      
# Task 5 — Missing Values 
print(df.isnull().sum())

missing_percent=(df.isnull().sum()/len(df)) * 100
print(missing_percent)

missing=df.isnull().sum()
print(missing[missing>0])

print(df[df.isnull().any(axis=1)])

# for numeric column
df["Sales"]=df["Sales"].fillna(df["Sales"].median()) 

# for categorical column
df["Category"]=df["Category"].fillna(df["Category"].mode()[0])

# for customer_id
df=df.dropna(subset=["Customer_ID"])

# Task 6 — Duplicate Records 
print("Duplicate records: ",df.duplicated().sum())

duplicates=df[df.duplicated()]
print("\nDuplicate rows: ")
print(duplicates)

df=df.drop_duplicates()

print("\nDuplicate records after cleaning: ",df.duplicated().sum())
print("Updated shape: ",df.shape)

# Task 7 — Create Data Dictionary
data_dictionary = pd.DataFrame({
    "Column Name": [
        "Order_ID",
        "Order_Date",
        "Customer_ID",
        "Customer_Name",
        "Product",
        "Category",
        "Region",
        "Quantity",
        "Unit_Price",
        "Discount",
        "Sales",
        "Cost",
        "Profit",
        "Payment_Method"
    ],

    "Data Type": [
        "Text/Integer",
        "Date",
        "Text",
        "Text",
        "Text",
        "Text",
        "Text",
        "Integer",
        "Float",
        "Float",
        "Float",
        "Float",
        "Float",
        "Text"
    ],

    "Description": [
        "Unique ID for each order",
        "Date when the order was placed",
        "Unique ID of the customer",
        "Name of the customer",
        "Name of the product purchased",
        "Category of the product",
        "Region where the sale occurred",
        "Number of units purchased",
        "Price of one unit of the product",
        "Discount given on the product/order",
        "Total sales or revenue generated",
        "Cost of the product/order",
        "Profit generated from the sale",
        "Payment method used by the customer"
    ]
})

print(data_dictionary)

print(data_dictionary.to_string(index=False))

data_dictionary.to_excel("data_dictionary.xlsx", index=False)
      