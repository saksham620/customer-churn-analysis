import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import mysql.connector

# conn = mysql.connector.connect(
#     host="127.0.0.1",
#     port=3306,
#     user="root",
#     password="Saksham@01",
#     database="customer_chrun"
# )

# print("MySQL connected successfully!")

# tables = pd.read_sql("SHOW TABLES", conn)

# for table_name in tables.iloc[:, 0]:
#     df = pd.read_sql(
#         f"SELECT * FROM `{table_name}`",
#         conn
#     )
#     globals()[f"df_{table_name}"] = df
#     print(f"\nCreated dataframe: df_{table_name}")
#     print(df.head())

# conn.close()


conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="Saksham@01",
    database="customer_chrun"
)
cursor = conn.cursor()

cursor.execute("""
    SELECT TABLE_NAME, COLUMN_NAME
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
    ORDER BY TABLE_NAME, ORDINAL_POSITION
""")

for table_name, column_name in cursor.fetchall():
    print(f"{table_name} → {column_name}")

#customer table data cleaning and go through data

query = "select * from db_customer"
df= pd.read_sql(query,conn)
print(df.head())

print(df.info())
print(df.tail())


# # rename col --- name
# # drop columns--- intrerst and pincode
# # change data type --- dob
# # fix data standarization of ---- gender
# # fix missing value  ---country

# rename col --- name
df.rename(columns={'name':'customer_name'}, inplace = True )
print(df.info())

# # drop columns--- intrerst and pincode
# print(df.drop(df.columns[-2:], axis=1))
print(df.drop(columns=['interests','pincode'], inplace=True))

# # change data type --- dob
df['dob'] = pd.to_datetime(
    df['dob'],
    format='%m/%d/%Y',
    errors='coerce'
)


# # fix data standarization of ---- gender
print(df['gender'].unique())

print(df['gender'].replace({'Men':'Male','Women':'Female'}))

# # fix missing value  ---country
print(df[df['country'].isna()])
print(df['country'].fillna('Nahi Ptta'))

print(df.dropna(subset=['country']).set_index('state')['country'].to_dict)

# #country and state- unique value pair

state_country_mapping = df.dropna(subset=['country']).set_index('state')['country'].to_dict()
df['country'] = df['country'].fillna(df['state'].map(state_country_mapping))

print("is null available")
print(df[df['country'].isna()])

print(df[['country','state']])




#subscription tables for data cleaning and go through

query = "select * from db_suscription"
df2= pd.read_sql(query,conn)
print(df2.head())

print(df2.info())
print(df2.tail())

date_col = ['subscription_start_date','renewal_date','cancellation_date']
df2[date_col] = df2[date_col].apply(pd.to_datetime, errors='coerce')
print(df2.info())



# support tables for data cleaning and go through it


query = "select * from db_support"
df3= pd.read_sql(query,conn)
print(df3.head())
print(df3.tail())


df3.drop(columns=['col_1','comment'], inplace=True)
print(df3.info())

df3['complaint_date'] = pd.to_datetime(df3['complaint_date'])
print(df3.info())



# Feature Engineering and Data Analysis
# create a new column using existing col - churn column
df2['churn_flag'] = np.where(df2['cancellation_date'].notna(),1,0)
print(df2.head())



# first fix support table duplicates then merge

df4 = (df2.merge(df, on = 'customerid', how='left')
   .merge(df3, on = 'customerid', how='left'))
# print(df4.head())
print(df4.info())

print(df2['customerid'].nunique())
print(df3['customerid'].nunique())
print(df['customerid'].nunique())

print(df3['customerid'].size)

df3['complaint_count'] = df3.groupby('customerid')['customerid'].transform('count')
print(df3.head())

df3 = df3.sort_values('complaint_date').drop_duplicates('customerid', keep='last')
print(df3.info())


print(df3['customerid'].size)

# merge data frame

df4 = (df2.merge(df, on = 'customerid', how='left')
   .merge(df3, on = 'customerid', how='left'))
print(df4.shape)

df4.to_csv('exported_churn_data.csv', index=False)

# Data Analysis
# 1. Churn Rate  

print(df4.columns)

churn_rate = df4['churn_flag'].mean()*100
print("churn Rate = ", round(churn_rate,2),"%")

# 2. Retention Rate

retention_rate = 100-churn_rate
print("Retention Rate = ", round(retention_rate,2),"%")

# 3. churn by plan type
churn_by_plan_type = (df4.groupby('plan_type')['churn_flag'].mean().mul(100).round(2).reset_index())
print("churn_by_plan_type = ",churn_by_plan_type)

#4. a-> churn by state -> sum(revenue) & count of users
churn_by_state = df4.groupby('state').agg(
    churn_count=('churn_flag','sum'),
    customer_count = ('customerid','count'),
    total_revenue = ('monthly_charges','sum')
).reset_index()
print("churn_by_state", churn_by_state)


#4. b-> churn by subscription type -> sum(revenue) & count of users

churn_by_subscription = df4.groupby('subscription_type').agg(
    churn_count=('churn_flag','sum'),
    customer_count = ('customerid','count'),
    total_revenue = ('monthly_charges','sum')
).reset_index()
print("churn_by_subscription", churn_by_subscription)

# 5. ARPU - Avg Revenue per User

avg_revenue = df4['monthly_charges'].mean().round(2)
print("avg_revenue =",avg_revenue)

# calculate customer age
customer_age = (pd.Timestamp.today()-df4['dob']).dt.days
print("customer_age", customer_age)

# 6. Avg Customer Tenure
# count number of days user has used our services : cancellation date else current date:

today = pd.Timestamp.today()
df4['tenure_days'] = np.where(
    df4['cancellation_date'].notna(),
(df4['cancellation_date']-df4['subscription_start_date']).dt.days,

(today - df4['subscription_start_date']).dt.days

)
print(df4.head(2))

Avg_Customer_Tenure = df4['tenure_days'].mean()
print("Avg_Customer_Tenure", round(Avg_Customer_Tenure),0)



# 7. Revenue at risk - revenue lost from churned users
Revenue_risk =df4.loc[df4['churn_flag'] ==1,'monthly_charges'].sum()
print(Revenue_risk)


# 8. Esclation Rate

Esclation_rate =(df4['escalations']=='Y').mean()*100
print("Esclation_rate", round(Esclation_rate,2),"%")


# 9. Avg Complain Rate per User

Avg_complaint = (df4['complaint_count'].sum() / df4['customerid'].nunique())
print("Avg Complaint Per User ",round(Avg_complaint,2))

# 10. Correlation Esclation vs Chrun

corr_df = df4[['escalations','churn_flag']].dropna()

df4['escalations']= np.where(df4['escalations']=='Y',1,0) # encoding string into int type
print(df4.head(2))

correlation = df4['escalations'].corr(df4['churn_flag'])
print("correlation percentage ",round(correlation,2))

# 11. churn risk - create a column using exisiting column

condition = [
    (df4['churn_score'] < 50),
    (df4['churn_score']>= 50)& (df4['churn_score']< 70),
    (df4['churn_score']>= 70)
]

choices= ['low','med','high']

df4['churn_risk'] = np.select(condition,choices, default='unknown')
print(df4[['churn_risk','churn_score']].head())



# 4. Visualization using Matplotlib

df_visual = df4.copy()

print(df_visual.head())

# 4.1 Monthly Churn Trends(Time Series KPI)

df_visual['cancellation_month'] = df_visual['cancellation_date'].dt.to_period('M')
churn_trend = df_visual[df_visual['churn_flag']==1].groupby('cancellation_month').size()

plt.figure(figsize=(8,3))
plt.plot(churn_trend.index.astype(str), churn_trend.values, color = 'green', marker='o', linestyle='dashed', linewidth=2, markersize = 12)
plt.title('Monthly Churn Trend')
plt.xlabel('Month')
plt.ylabel('Churned Customers')
plt.show()


#4. 2 Churn  by Plan Type
churn_plan = df_visual.groupby('plan_type')['churn_flag'].mean()

colours = ['#1E3A8A' , '#2563EB' , '#60A5FA']
plt.figure(figsize=(7,4))
plt.bar(churn_plan.index, churn_plan.values, color = colours)
plt.show()


# 4.3 Churn by States

churn_state = df_visual.groupby('state')['churn_flag'].mean()
colours1 = ['#334155' , '#64748B' , '#94A3B8' , '#3B82F6']
plt.figure(figsize=(17,7))
plt.bar(churn_state.index, churn_state.values, color = colours1)
plt.show()

 # using Sea-Born library 

# incorrect method of encoding -  as number are not assigned based on priority


df_encoded = df_visual[['plan_type','contract_type','churn_score','churn_flag','churn_risk','escalations']]

categorial_cols = ['plan_type','contract_type','churn_risk']

for col in categorial_cols:
    df_encoded[col] = df_encoded[col].astype('category').cat.codes


print(df_encoded.head())

sns.heatmap(df_encoded.corr(),annot=True)
plt.show()


# now correct method for encoding

df_encoded = df_visual[['plan_type','contract_type','churn_score','churn_flag','churn_risk','escalations']]

order_mapping = {'plan_type': ['Basic','Standard','Premium'],
                 'contract_type':['Monthly','Annual'],
                 'churn_risk':['low','med','high']
                 }

for col , order in order_mapping.items():
    df_encoded[col] = pd.Categorical(df_encoded[col].astype('category'), categories= order, ordered=True).codes

print(df_encoded.head())

sns.heatmap(df_encoded.corr(),annot=True)
plt.show()


# Pivot Table

pd.pivot_table(
    df_visual,
    values='churn_flag',
    index='plan_type',
    aggfunc='mean'
)

pd.pivot_table(
    df_visual,
    index='plan_type',
    values=['monthly_charges','customerid','churn_flag'],
    aggfunc={
        'monthly_charges':'sum',
        'customerid':'nunique',
        'churn_flag':'mean'
    }
)

# for closing the connection between sql and python

conn.close()

