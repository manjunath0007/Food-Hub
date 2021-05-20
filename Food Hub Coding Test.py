#!/usr/bin/env python
# coding: utf-8



# importing the packages
import pandas as pd
import numpy as np


# reading the csv files
orders = pd.read_csv('orders_test (2).csv')
stores = pd.read_csv('store_test (2).csv')
customers = pd.read_csv('customer_test (2).csv')


# 1. Create a CSV containing an aggregate table showing the total orders and revenue
# each store had each month. It should have the following columns:
# 
# Year (Eg: 2020)
# 
# Month (Eg: January)
# 
# Store Name
# 
# Number of Orders
# 
# Total Revenue
# 


# renaming, creating, merging columns as per required output
stores.rename(columns={'id':'store_id'},inplace=True)
orders['order_date'] = pd.to_datetime(orders['order_date'])
orders['Year'] = orders['order_date'].apply(lambda x : x.strftime('%Y'))
orders['Month'] = orders['order_date'].apply(lambda x : x.strftime('%B'))
store_orders = stores.merge(orders, on=['store_id'], how = 'left')



store_orders.groupby(['name','Year','Month']).agg({'id':'count','total':'sum'}).reset_index().rename(columns={
                    'name':'Store Name','id':'Number of Orders','total':'Total revenue'})


# storing the csv for question 1 reesults
Q1 = store_orders.groupby(['name','Year','Month']).agg({'id':'count','total':'sum'}).reset_index().rename(columns={
                    'name':'Store Name','id':'Number of Orders','total':'Total revenue'})
Q1.to_csv('Q1.csv')


# 2. Create a CSV containing a list of users who have placed less than 10 orders. It should have the following columns:
# 
# First Name
# 
# Last Name
# 
# Email
# 
# Orders Placed by user
# 


# renaming, merging columns as per required output
customers.rename(columns={'id':'customer_id'},inplace=True)
customer_orders = customers.merge(orders,on='customer_id',how='left')
customers_with_orders = customer_orders.groupby(['first_name','last_name','email']).agg({'id':'count'}).reset_index().rename(
    columns={'first_name':'First Name','last_name':'Last Name','email':'Email','id':'Orders Placed by user'})


# pulling customer info who has ordered less than 10 orders
customers_with_lt_10_orders = customers_with_orders[customers_with_orders['Orders Placed by user'] < 10]


# saving the results of Q2
customers_with_lt_10_orders.to_csv('Q2.csv')


# 3. In question 2, use a MD5 hash to encrypt the emails of the users before converting it to CSV.

# importing the hash library
import hashlib

# hasing the Email information of customer
customers_with_lt_10_orders['Email']=customers_with_lt_10_orders.Email.apply(lambda x: hashlib.md5(x.encode()).hexdigest())


# stroing the customer order info with hashed Email information 
customers_with_lt_10_orders.to_csv('Q3.csv')

