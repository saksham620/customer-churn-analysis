
# Customer Churn Analysis using MySQL and Python

## Project Overview
This project focuses on analyzing customer churn to understand customer behavior, subscription patterns, cancellations, and factors associated with customer retention. MySQL is used for data storage and SQL-based analysis, while Python is used for data cleaning, exploratory data analysis, and visualization.

The goal is to identify useful patterns in customer churn and generate insights that can support better customer retention strategies.

## Objectives
- Analyze customer and subscription information.
- Identify customer churn patterns and cancellation trends.
- Explore subscription types, contract types, and monthly charges.
- Analyze customer support information and satisfaction scores.
- Visualize churn trends and communicate findings through charts.

## Tools & Technologies
- **MySQL:** Data storage, SQL queries, filtering, aggregation, and analysis.
- **Python:** Data analysis and visualization.
- **Pandas:** Data cleaning and manipulation.
- **NumPy:** Numerical operations.
- **Matplotlib:** Data visualization.
- **Seaborn:** Statistical visualizations and heatmaps.
- **VS Code:** Development environment.

## Dataset
The project uses customer-related data organized into three tables:

- `db_customer` — customer details and demographics.
- `db_suscription` — subscription details, charges, cancellation information, and churn-related fields.
- `db_support` — customer complaints, escalations, and satisfaction scores.

*Note: The table names above reflect the names used in the project database.*

## Project Workflow
1. Connected Python to the MySQL database.
2. Retrieved tables for analysis using Pandas.
3. Inspected data types, missing values, and data quality.
4. Prepared customer and subscription data for analysis.
5. Analyzed churn patterns using SQL and Python.
6. Created visualizations to explore cancellation trends and customer behavior.
7. Interpreted the results to identify potential customer retention opportunities.

## Analysis & Visualizations
The project explores:
- Monthly customer cancellation trends.
- Customer demographics and subscription characteristics.
- Monthly charges and customer lifetime value.
- Customer satisfaction and support-related patterns.
- Relationships between customer attributes and churn.

## Key Findings
Add your actual results here after completing the analysis. For example:
- Which customer segment has the highest churn rate?
- Which contract or subscription type is associated with more cancellations?
- How do monthly charges differ between churned and retained customers?
- Which customer support patterns are associated with churn?

*Only include findings supported by your actual data and analysis.*

## Skills Demonstrated
- SQL querying and data aggregation
- MySQL database connectivity
- Data cleaning and preprocessing
- Exploratory data analysis (EDA)
- Python data analysis using Pandas and NumPy
- Data visualization using Matplotlib and Seaborn
- Translating data patterns into business insights

## How to Run the Project
1. Clone or download this repository.
2. Install Python and MySQL.
3. Install the required Python libraries:
   ```bash
   pip install pandas numpy matplotlib seaborn mysql-connector-python
   ```
4. Configure your MySQL connection using your own local database credentials.
5. Make sure the required tables and data are available in MySQL.
6. Run the Python analysis script:
   ```bash
   python chun_analysis.py
   ```

## Future Improvements
- Build an interactive Power BI dashboard.
- Add automated data quality checks.
- Develop customer churn risk segments.
- Create recommendations based on verified analysis results.

## Author
Data Analytics Project | MySQL • Python • Pandas • Data Visualization
