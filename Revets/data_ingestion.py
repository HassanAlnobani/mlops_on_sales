"""
data_ingestion.py
==================
This script handles loading, cleaning, and saving sales data to an SQLite database.
It also includes queries to calculate useful insights like average order value 
and monthly revenue.
"""

import pandas as pd  # To handle data operations like loading and cleaning
import sqlite3       # To interact with the SQLite database

def load_and_clean_data(file_path):
    """
    Load data from a CSV file and clean it up.

    Steps:
    - Rename columns to make them easier to work with.
    - Convert date columns to the proper datetime format.
    - Fill missing values in specific columns.

    Args:
        file_path (str): Path to the CSV file containing sales data.

    Returns:
        pd.DataFrame: A cleaned DataFrame ready for further processing.
    """
    # Load the CSV data into a DataFrame
    data = pd.read_csv(file_path)
    
    # Standardize column names (remove extra spaces, use lowercase, replace spaces with underscores)
    data.columns = data.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Convert date columns from text to datetime objects
    # The dataset uses DD/MM/YYYY, so we set dayfirst=True
    data['order_date'] = pd.to_datetime(data['order_date'], dayfirst=True)
    data['ship_date'] = pd.to_datetime(data['ship_date'], dayfirst=True)

    # Fill missing values:
    # - Replace missing postal codes with 'Unknown'
    # - Set missing profit values to 0
    data.fillna({'postal_code': 'Unknown', 'profit': 0}, inplace=True)

    # Return the cleaned DataFrame
    return data

def save_to_database(data, db_path):
    """
    Save the cleaned data to an SQLite database.

    Args:
        data (pd.DataFrame): The cleaned sales data as a DataFrame.
        db_path (str): Path to the SQLite database file.
    """
    # Connect to the SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect(db_path)

    # Save the data as a table named 'sales'. If the table exists, it will be replaced.
    data.to_sql("sales", conn, if_exists="replace", index=False)

    # Commit the changes to the database and close the connection
    conn.commit()
    conn.close()

def get_average_order_value(db_path):
    """
    Calculate the average value of an order from the database.

    Args:
        db_path (str): Path to the SQLite database file.

    Returns:
        float: The average value of an order.
    """
    # Connect to the database
    conn = sqlite3.connect(db_path)

    # Run a SQL query to calculate the average value of sales
    query = "SELECT AVG(sales) AS avg_order_value FROM sales"
    result = conn.execute(query).fetchone()

    # Close the connection
    conn.close()

    # Return the average order value (first column of the result)
    return result[0]

def get_average_revenue_per_month(db_path):
    """
    Calculate the total sales revenue for each month from the database.

    Args:
        db_path (str): Path to the SQLite database file.

    Returns:
        list: A list of tuples where each tuple contains a month and its total revenue.
    """
    # Connect to the database
    conn = sqlite3.connect(db_path)

    # SQL query to calculate total sales grouped by month
    query = """
        SELECT 
            strftime('%Y-%m', order_date) AS month, 
            SUM(sales) AS sales_revenue
        FROM sales
        GROUP BY month
    """
    result = conn.execute(query).fetchall()

    # Close the connection
    conn.close()

    # Return the list of results (month, revenue)
    return result

if __name__ == "__main__":
    """
    Main program entry point. Handles data processing and displays insights.
    """
    # Define the file path for the CSV data and the SQLite database
    file_path = "sales.csv"  # Update the path if the file is in a different location
    db_path = "sales.db"     # Name of the database file to create or use

    # Step 1: Load and clean the sales data from the CSV file
    data = load_and_clean_data(file_path)

    # Step 2: Save the cleaned data into the SQLite database
    save_to_database(data, db_path)

    # Step 3: Query the average value of an order and print it
    avg_order_value = get_average_order_value(db_path)
    print(f"Average Order Value: {avg_order_value}")

    # Step 4: Query the total revenue for each month and print it
    avg_revenue_per_month = get_average_revenue_per_month(db_path)
    print("Average Revenue per Month:")
    for month, revenue in avg_revenue_per_month:
        print(f"{month}: {revenue}")
