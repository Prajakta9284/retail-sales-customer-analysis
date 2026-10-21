import pandas as pd
from pathlib import Path

# --------------------------------------------------
# Retail Sales Business Recommendations - Day 33
# --------------------------------------------------

from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_DIR / "data" / "retail_sales_cleaned.csv"
OUTPUT_FILE = PROJECT_DIR / "excel" / "business_recommendations.csv"

# Search common locations: script folder, project folder, and terminal folder.
possible_inputs = [
    PROJECT_DIR / "data" / "retail_sales_cleaned.csv",
    PROJECT_DIR / "retail_sales_cleaned.csv",
    Path.cwd() / "retail_sales_cleaned.csv",
]
INPUT_FILE = next((path for path in possible_inputs if path.exists()), None)

if INPUT_FILE is None:
    locations = "\n".join(f"- {path}" for path in possible_inputs)
    raise FileNotFoundError(
        "Could not find retail_sales_cleaned.csv. Checked these locations:\n"
        f"{locations}\n\n"
        "Move/copy retail_sales_cleaned.csv into the Retail Project folder "
        "or the python folder, then run the script again."
    )

df = pd.read_csv(INPUT_FILE)
df.columns = df.columns.str.strip()

# Convert available numeric columns safely
for col in ["Sales", "Profit", "Quantity", "Discount", "Unit_Price"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

if "Order_Date" in df.columns:
    df["Order_Date"] = pd.to_datetime(
        df["Order_Date"], errors="coerce", dayfirst=True
    )

recommendations = []


def add_recommendation(finding, evidence, impact, recommendation):
    """Add one business recommendation to the report."""
    recommendations.append({
        "Finding": finding,
        "Evidence": evidence,
        "Impact": impact,
        "Recommendation": recommendation
    })


def money(value):
    return f"{value:,.2f}"


def profit_margin(data):
    """Calculate overall profit margin using total profit / total sales."""
    sales = data["Sales"].sum()
    if sales == 0 or pd.isna(sales):
        return None
    return (data["Profit"].sum() / sales) * 100


# Check for the essential columns
required = {"Sales", "Profit"}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing required column(s): {', '.join(sorted(missing))}")

# Remove rows where essential measures are unavailable
df = df.dropna(subset=["Sales", "Profit"]).copy()

if df.empty:
    raise ValueError("No valid rows found for Sales and Profit.")

# 1. Product profitability
if "Product" in df.columns:
    product_summary = (
        df.groupby("Product", dropna=False)
        .agg(Total_Sales=("Sales", "sum"), Total_Profit=("Profit", "sum"))
        .reset_index()
    )
    product_summary = product_summary[product_summary["Total_Sales"] != 0]
    if not product_summary.empty:
        product_summary["Profit_Margin"] = (
            product_summary["Total_Profit"] / product_summary["Total_Sales"] * 100
        )
        item = product_summary.sort_values("Profit_Margin").iloc[0]
        add_recommendation(
            f"{item['Product']} has the lowest product profit margin",
            f"Sales: {money(item['Total_Sales'])}; profit: {money(item['Total_Profit'])}; "
            f"margin: {item['Profit_Margin']:.2f}%",
            "Low margins can limit the profit earned from sales.",
            "Review pricing, supplier costs and discounts. Check whether changes improve "
            "profitability without causing a large fall in sales."
        )
    else:
        add_recommendation(
            "Product profitability could not be compared",
            "Product sales totals were zero or unavailable.",
            "Management cannot reliably identify the most profitable products.",
            "Check product sales and profit data, then repeat the product-level analysis."
        )

# 2. High-value customers
if "Customer_ID" in df.columns:
    customer_summary = (
        df.groupby("Customer_ID", dropna=False)
        .agg(Total_Sales=("Sales", "sum"), Total_Profit=("Profit", "sum"))
        .reset_index()
    )
    if not customer_summary.empty:
        item = customer_summary.sort_values("Total_Sales", ascending=False).iloc[0]
        add_recommendation(
            f"Customer {item['Customer_ID']} is the highest-value customer by sales",
            f"Customer sales: {money(item['Total_Sales'])}; "
            f"customer profit: {money(item['Total_Profit'])}",
            "Losing a major customer could reduce revenue.",
            "Consider a loyalty offer and personalized service, while checking customer "
            "profitability before offering discounts."
        )

# 3. Category performance / decline
if "Category" in df.columns and "Order_Date" in df.columns:
    dated = df.dropna(subset=["Order_Date"]).copy()
    if not dated.empty:
        dated["Month"] = dated["Order_Date"].dt.to_period("M")
        monthly_category = (
            dated.groupby(["Category", "Month"])["Sales"].sum().reset_index()
        )
        months = sorted(monthly_category["Month"].unique())
        if len(months) >= 2:
            latest_month, previous_month = months[-1], months[-2]
            recent = monthly_category[monthly_category["Month"] == latest_month]
            previous = monthly_category[monthly_category["Month"] == previous_month]
            comparison = recent.merge(
                previous, on="Category", how="outer",
                suffixes=("_latest", "_previous")
            ).fillna(0)
            comparison["Growth_Pct"] = comparison.apply(
                lambda r: (
                    (r["Sales_latest"] - r["Sales_previous"])
                    / abs(r["Sales_previous"]) * 100
                    if r["Sales_previous"] != 0 else float("nan")
                ),
                axis=1
            )
            declining = comparison.dropna(subset=["Growth_Pct"]).sort_values("Growth_Pct")
            if not declining.empty:
                item = declining.iloc[0]
                add_recommendation(
                    f"Category {item['Category']} has the largest sales decline",
                    f"Sales changed from {money(item['Sales_previous'])} in "
                    f"{previous_month} to {money(item['Sales_latest'])} in "
                    f"{latest_month} ({item['Growth_Pct']:.2f}%).",
                    "A continued decline may reduce category revenue.",
                    "Investigate demand, product availability, competitor activity and pricing. "
                    "Test targeted promotions and monitor the next month's results."
                )
            else:
                add_recommendation(
                    "Category sales could not be compared for growth",
                    "The previous month had no non-zero sales baseline for comparison.",
                    "A reliable decline trend cannot be established from this comparison.",
                    "Review category sales across more months before making changes."
                )
        else:
            add_recommendation(
                "There is not enough monthly history to identify declining categories",
                "Fewer than two distinct months were found in Order_Date.",
                "A sales decline cannot be confirmed from a single month.",
                "Collect or analyze at least two months of sales data and compare categories."
            )

# 4. Regional profitability
if "Region" in df.columns:
    region_summary = (
        df.groupby("Region", dropna=False)
        .agg(Total_Sales=("Sales", "sum"), Total_Profit=("Profit", "sum"))
        .reset_index()
    )
    region_summary = region_summary[region_summary["Total_Sales"] != 0]
    if not region_summary.empty:
        region_summary["Profit_Margin"] = (
            region_summary["Total_Profit"] / region_summary["Total_Sales"] * 100
        )
        item = region_summary.sort_values("Profit_Margin").iloc[0]
        add_recommendation(
            f"Region {item['Region']} has the lowest regional profit margin",
            f"Sales: {money(item['Total_Sales'])}; profit: {money(item['Total_Profit'])}; "
            f"margin: {item['Profit_Margin']:.2f}%",
            "Low regional profitability may weaken overall business performance.",
            "Review regional discounts, delivery and operating costs, product mix, and local "
            "demand before deciding how to improve performance."
        )

# 5. Customer retention / repeat purchasing
if "Customer_ID" in df.columns:
    customer_orders = df.groupby("Customer_ID")[
        "Order_ID" if "Order_ID" in df.columns else "Sales"
    ].nunique()
    total_customers = len(customer_orders)
    repeat_customers = int((customer_orders > 1).sum())
    repeat_pct = repeat_customers / total_customers * 100 if total_customers else 0
    add_recommendation(
        "Customer repeat-purchase behavior should be monitored",
        f"{repeat_customers} of {total_customers} customers have more than one "
        f"distinct {'order' if 'Order_ID' in df.columns else 'sales value'} "
        f"({repeat_pct:.2f}%).",
        "Low repeat purchasing may increase reliance on acquiring new customers.",
        "Track repeat purchase rate over time, contact inactive customers where dates permit, "
        "and test relevant loyalty or re-engagement campaigns."
    )

# 6. Discount and profitability relationship
if "Discount" in df.columns:
    discount_data = df.dropna(subset=["Discount"]).copy()
    if len(discount_data) >= 4 and discount_data["Discount"].nunique() >= 2:
        try:
            discount_data["Discount_Group"] = pd.qcut(
                discount_data["Discount"], q=2,
                labels=["Lower-discount orders", "Higher-discount orders"],
                duplicates="drop"
            )
            discount_summary = (
                discount_data.groupby("Discount_Group", observed=True)
                .apply(
                    lambda g: pd.Series({
                        "Sales": g["Sales"].sum(),
                        "Profit": g["Profit"].sum(),
                        "Margin": profit_margin(g)
                    }),
                    include_groups=False
                )
                .dropna(subset=["Margin"])
            )
            if len(discount_summary) >= 2:
                low = discount_summary.iloc[0]
                high = discount_summary.iloc[-1]
                add_recommendation(
                    "Compare profitability of lower- and higher-discount orders",
                    f"Lower-discount margin: {low['Margin']:.2f}%; "
                    f"higher-discount margin: {high['Margin']:.2f}%.",
                    "Large discounts may reduce profit even when sales are generated.",
                    "Review discount rules and compare profit as well as sales before continuing "
                    "promotions. This comparison is observational, not proof that discounts "
                    "caused the margin difference."
                )
            else:
                raise ValueError("Insufficient discount groups")
        except (ValueError, TypeError):
            add_recommendation(
                "Discount impact could not be reliably compared",
                "Discount data did not form two usable groups.",
                "The effect of discount levels on profitability remains unclear.",
                "Check discount values and compare sales and profit across discount ranges."
            )
    else:
        add_recommendation(
            "Discount data is insufficient for a reliable comparison",
            "Too few valid discount records or distinct discount values were available.",
            "The effect of discounting on profit is unclear.",
            "Validate discount data and analyze profitability across discount levels."
        )
else:
    add_recommendation(
        "Discount impact cannot be evaluated",
        "The dataset does not contain a Discount column.",
        "The contribution of discounts to profit cannot be measured.",
        "Add discount information to the dataset and compare margins across discount levels."
    )

# 7. Slow-selling products (sales/quantity is a proxy, not actual stock data)
if "Product" in df.columns:
    product_metrics = {"Sales": ("Sales", "sum")}
    if "Quantity" in df.columns:
        product_metrics["Quantity"] = ("Quantity", "sum")
    slow_products = df.groupby("Product", dropna=False).agg(**product_metrics).reset_index()
    metric = "Quantity" if "Quantity" in df.columns else "Sales"
    if not slow_products.empty:
        item = slow_products.sort_values(metric).iloc[0]
        add_recommendation(
            f"{item['Product']} has the lowest recorded sales volume",
            f"Total {metric.lower()}: {money(item[metric])}; "
            f"total sales: {money(item['Sales'])}.",
            "Persistently weak demand can make inventory planning less efficient.",
            "Review demand and reorder quantities for this product. Confirm actual stock levels "
            "before labeling it overstocked or slow-moving inventory."
        )

# 8. Marketing allocation proxy based on category performance
if "Category" in df.columns:
    category_summary = (
        df.groupby("Category", dropna=False)
        .agg(Total_Sales=("Sales", "sum"), Total_Profit=("Profit", "sum"))
        .reset_index()
    )
    if not category_summary.empty:
        item = category_summary.sort_values("Total_Profit", ascending=False).iloc[0]
        add_recommendation(
            f"Category {item['Category']} contributes the highest total profit",
            f"Sales: {money(item['Total_Sales'])}; profit: {money(item['Total_Profit'])}.",
            "Category performance can help guide where to test marketing activity.",
            "Consider a small, measurable campaign for this category and track campaign costs, "
            "incremental sales and profit before increasing the budget. Marketing ROI is not "
            "available from the current sales data alone."
        )

# 9. Product strategy: lowest total profit
if "Product" in df.columns:
    product_profit = (
        df.groupby("Product", dropna=False)
        .agg(Total_Sales=("Sales", "sum"), Total_Profit=("Profit", "sum"))
        .reset_index()
    )
    if not product_profit.empty:
        item = product_profit.sort_values("Total_Profit").iloc[0]
        add_recommendation(
            f"{item['Product']} has the lowest total profit",
            f"Total profit: {money(item['Total_Profit'])}; "
            f"total sales: {money(item['Total_Sales'])}.",
            "Products with weak or negative profit may use resources without sufficient return.",
            "Investigate costs, pricing and demand. Consider improving or discontinuing the product "
            "only after reviewing trends and strategic importance."
        )

# 10. Regional expansion opportunity
if "Region" in df.columns:
    region_summary = (
        df.groupby("Region", dropna=False)
        .agg(Total_Sales=("Sales", "sum"), Total_Profit=("Profit", "sum"))
        .reset_index()
    )
    if not region_summary.empty:
        item = region_summary.sort_values("Total_Profit", ascending=False).iloc[0]
        margin = (
            item["Total_Profit"] / item["Total_Sales"] * 100
            if item["Total_Sales"] != 0 else float("nan")
        )
        add_recommendation(
            f"Region {item['Region']} has the highest total profit",
            f"Sales: {money(item['Total_Sales'])}; profit: {money(item['Total_Profit'])}; "
            f"margin: {margin:.2f}%.",
            "The region may offer useful lessons for improving performance elsewhere.",
            "Study the region's customer demand and product mix. Test expansion in a comparable "
            "market on a small scale before committing significant resources."
        )

# Save a compact report (usually only 10 rows)
report = pd.DataFrame(
    recommendations,
    columns=["Finding", "Evidence", "Impact", "Recommendation"]
)

report.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print("\n" + "=" * 65)
print("RETAIL SALES BUSINESS RECOMMENDATIONS")
print("=" * 65)
print(f"Valid sales records analyzed: {len(df)}")
print(f"Recommendations generated: {len(report)}")
print(f"Report saved to: {OUTPUT_FILE.resolve()}")
print("\nPreview:\n")
for index, row in report.iterrows():
    print(f"{index + 1}. Finding: {row['Finding']}")
    print(f"   Evidence: {row['Evidence']}")
    print(f"   Impact: {row['Impact']}")
    print(f"   Recommendation: {row['Recommendation']}\n")
