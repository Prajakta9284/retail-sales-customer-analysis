
import pandas as pd

df = pd.read_csv(
    r"C:\Users\praja\OneDrive\Desktop\Retail Project\data\retail_sales_cleaned.csv"
)
df["Order_Date"] = pd.to_datetime(
    df["Order_Date"], errors="coerce", dayfirst=True
)
for col in ["Sales", "Profit", "Quantity"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["Sales", "Profit", "Order_Date"])

product = df.groupby("Product").agg(
    Revenue=("Sales", "sum"),
    Profit=("Profit", "sum"),
    Quantity=("Quantity", "sum")
)
product["Margin"] = (
    product["Profit"] / product["Revenue"].replace(0, float("nan")) * 100
)

category = df.groupby("Category").agg(
    Revenue=("Sales", "sum"),
    Profit=("Profit", "sum")
)
category["Margin"] = (
    category["Profit"] / category["Revenue"].replace(0, float("nan")) * 100
)

region = df.groupby("Region").agg(
    Revenue=("Sales", "sum"),
    Profit=("Profit", "sum")
)
region["Margin"] = (
    region["Profit"] / region["Revenue"].replace(0, float("nan")) * 100
)

monthly = df.groupby(df["Order_Date"].dt.to_period("M"))["Sales"].sum()
customer_orders = df.groupby("Customer_ID")["Order_ID"].nunique()
customer_revenue = df.groupby("Customer_ID")["Sales"].sum()

insights = []

def add(finding, evidence, impact):
    insights.append({
        "Finding": finding,
        "Evidence": evidence,
        "Business Impact": impact
    })

# 1. Highest revenue region
r = region["Revenue"].idxmax()
add(
    f"{r} has the highest sales",
    f"Revenue: ₹{region.loc[r, 'Revenue']:,.2f}",
    "Strong market; maintain successful regional strategies."
)

# 2. Lowest revenue region
r = region["Revenue"].idxmin()
add(
    f"{r} is the lowest-performing region by sales",
    f"Revenue: ₹{region.loc[r, 'Revenue']:,.2f}",
    "Investigate local demand, distribution, and marketing."
)

# 3. Highest-selling product
p = product["Revenue"].idxmax()
add(
    f"{p} is the top product by revenue",
    f"Revenue: ₹{product.loc[p, 'Revenue']:,.2f}",
    "Protect stock availability and evaluate expansion opportunities."
)

# 4. High-sales product with the lowest margin
high_sales = product[product["Revenue"] >= product["Revenue"].median()]
valid_margin = high_sales.dropna(subset=["Margin"])
if not valid_margin.empty:
    p = valid_margin["Margin"].idxmin()
    add(
        f"{p} has relatively high sales but the lowest margin among high-sales products",
        f"Revenue: ₹{product.loc[p, 'Revenue']:,.2f}; "
        f"margin: {product.loc[p, 'Margin']:.2f}%",
        "Review pricing, discounts, and product costs."
    )

# 5. Highest-revenue category
c = category["Revenue"].idxmax()
add(
    f"{c} is the leading category by revenue",
    f"Revenue: ₹{category.loc[c, 'Revenue']:,.2f}",
    "Prioritize inventory and marketing where profitable."
)

# 6. Lowest-margin category
valid_category = category.dropna(subset=["Margin"])
if not valid_category.empty:
    c = valid_category["Margin"].idxmin()
    add(
        f"{c} has the lowest category profit margin",
        f"Margin: {category.loc[c, 'Margin']:.2f}%; "
        f"profit: ₹{category.loc[c, 'Profit']:,.2f}",
        "Review costs, discounting, and product mix."
    )

# 7. Monthly sales trend
if len(monthly) >= 2:
    previous, latest = monthly.iloc[-2], monthly.iloc[-1]
    change = (latest - previous) / abs(previous) * 100 if previous != 0 else None
    if change is not None:
        direction = "increased" if change >= 0 else "declined"
        add(
            f"Sales {direction} in the latest month compared with the previous month",
            f"Previous: ₹{previous:,.2f}; latest: ₹{latest:,.2f}; "
            f"change: {change:.2f}%",
            "Use the trend to plan inventory, promotions, and sales targets."
        )

# 8. Most profitable product
p = product["Profit"].idxmax()
add(
    f"{p} generates the highest total profit",
    f"Profit: ₹{product.loc[p, 'Profit']:,.2f}",
    "Prioritize products that contribute strongly to profitability."
)

# 9. Repeat customers
repeat = customer_orders[customer_orders > 1]
total_customers = customer_orders.nunique()
repeat_share = len(repeat) / total_customers * 100 if total_customers else 0
add(
    "Repeat-customer performance",
    f"{len(repeat)} repeat customers out of {total_customers}; "
    f"{repeat_share:.2f}% of customers placed multiple orders",
    "Use loyalty programs and targeted offers to encourage repeat purchases."
)

# 10. Revenue contribution from top customers
if not customer_revenue.empty and customer_revenue.sum() != 0:
    top_customer = customer_revenue.idxmax()
    share = customer_revenue.loc[top_customer] / customer_revenue.sum() * 100
    add(
        f"Customer {top_customer} contributes the most revenue",
        f"Revenue: ₹{customer_revenue.loc[top_customer]:,.2f}; "
        f"share of total revenue: {share:.2f}%",
        "Strengthen retention while reducing dependence on individual customers."
    )



report = pd.DataFrame(insights)
report.insert(0, "Insight No.", range(1, len(report) + 1))

print("\nRETAIL SALES BUSINESS INSIGHTS")
print("=" * 80)
print(report.to_string(index=False))

report.to_csv("business_insights.csv", index=False)
print("\nSaved report: business_insights.csv")
print(f"Total insights generated: {len(report)}")
