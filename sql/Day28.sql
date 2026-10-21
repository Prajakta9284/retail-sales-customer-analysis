create database retail_analysis;

use retail_analysis;

select * from retail_sales limit 10;

select count(*) as total_rows from retail_sales_new;

select * from retail_sales_new limit 10;

-- basic

select sum(Sales) as total_sales from retail_sales_new;

select sum(Profit) as total_profit from retail_sales_new;

select count(distinct Order_ID) as total_orders from retail_sales_new;

select count(distinct Customer_ID) as total_customers from retail_sales_new;

select sum(Sales) / count(distinct Order_ID) as average_order_value from retail_sales_new;

-- grouping

select Category, sum(Sales) as total_sales 
from retail_sales_new group by Category order by total_sales desc;

select Region, sum(Sales) as total_sales 
from retail_sales_new group by Region order by total_sales desc;

select Category, sum(Profit) as total_profit 
from retail_sales_new group by Category order by total_profit desc;

select Region, sum(Profit) as total_profit 
from retail_sales_new group by Region order by total_profit desc;

select month(Order_Date) as month_number, monthname(Order_Date) as month_name, sum(Sales) as total_sales
from retail_sales_new group by month(Order_Date), monthname(Order_Date) order by month_number;

select
 year(Order_Date) as sales_year,
 month(Order_Date) as month_number,
 monthname(Order_Date) as month_name,
 sum(Sales) as total_sales
from retail_sales_new
 group by
 year(Order_Date),
 month(Order_Date),
 monthname(Order_Date)
 order by sales_year, month_number;
 
 -- customer
 
 select
 Customer_ID,
 Customer_Name,
 sum(Sales) as total_Sales
 from retail_sales_new
 group by Customer_ID, Customer_Name
 order by total_sales desc
 limit 10;
 
 
select 
Customer_ID,
Customer_Name,
count(distinct Order_ID) as total_orders,
sum(Sales) as total_spending
from retail_sales_new 
group by Customer_ID, Customer_Name
having count(distinct Order_ID) > 1
order by total_orders desc;

select 
round(avg(Customer_Spending), 2) as average_customer_spending
from (
select 
Customer_ID,
sum(Sales) as customer_spending
from retail_sales_new 
group by Customer_ID
) as customer_totals;

-- product

select 
Product,
sum(Sales) as total_sales
from retail_sales_new
group by Product 
order by total_sales desc 
limit 10;

select 
Product,
sum(Sales) as total_sales
from retail_sales_new
group by Product 
order by total_sales asc
limit 10;

select 
Product,
sum(Sales) as total_sales,
sum(Profit) as total_profit
from retail_sales_new 
group by Product 
order by total_profit desc 
limit 10;

-- advanced

select 
Customer_ID,
Customer_Name,
sum(Sales) as total_sales,
rank() over(
order by sum(Sales) desc
) as customer_rank
from retail_sales_new
group by Customer_ID, Customer_Name;

select 
Product,
sum(Sales) as total_sales,
dense_rank() over(
order by sum(Sales) desc
) as product_rank
from retail_sales new
group by Product;

with Monthly_Sales as (
select 
date_format(Order_Date, '%Y-%m') as sales_month,
sum(Sales) as total_sales
from retail_sales_new 
group by date_format(Order_Date, '%Y-%m')
),
previous_month as (
select 
sales_month,
total_sales,
lag(total_sales) over(
order by sales_month
) as previous_month_sales
from Monthly_Sales
)
select
sales_month,
total_sales,
previous_month_sales,
round(
(total_sales - previous_month_sales) 
/ nullif(previous_month_sales, 0) * 100,
2
) as growth_percentage
from previous_month
order by sales_month;

select 
Category,
sum(Sales) as total_sales,
rank() over(
order by sum(Sales) desc
) as category_rank 
from retail_sales_new
group by Category;



