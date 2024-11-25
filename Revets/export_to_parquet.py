"""
export_to_parquet.py
====================
This script exports the "sales" table from an SQLite database into a Parquet file for efficient storage and analysis.
"""

import pandas as pd  # Used for handling and exporting data
import sqlite3       # Used for interacting with the SQLite database

def export_to_parquet(db_path, parquet_path):
    """
    Export the "sales" table from the SQLite database to a Parquet file.

    Args:
        db_path (str): Path to the SQLite database file.
        parquet_path (str): Path to the output Parquet file.

    Steps:
    - Connect to the SQLite database.
    - Read the "sales" table into a Pandas DataFrame.
    - Save the DataFrame as a Parquet file.

    Returns:
        None
    """
    # Step 1: Connect to the SQLite database
    conn = sqlite3.connect(db_path)

    # Step 2: Read the "sales" table into a DataFrame
    query = "SELECT * FROM sales"  # SQL query to fetch all data from the "sales" table
    data = pd.read_sql(query, conn)

    # Step 3: Close the database connection
    conn.close()

    # Step 4: Export the DataFrame to a Parquet file
    # Parquet is a columnar storage file format, ideal for large datasets
    data.to_parquet(parquet_path, index=False)

    # Notify the user that the export is complete
    print(f"Data successfully exported to {parquet_path}.")

if __name__ == "__main__":
    """
    Main program entry point. Sets up file paths and calls the export function.
    """
    # Path to the SQLite database file
    db_path = "sales.db"

    # Path where the Parquet file will be saved
    parquet_path = "sales.parquet"

    # Export the sales table to a Parquet file
    export_to_parquet(db_path, parquet_path)
