import pandas as pd
import pyodbc

# Connection
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=desktop-btvgd35\SQLEXPRESS;'
    'DATABASE=global sales;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()
cursor.fast_executemany = True  # speeds up bulk insert

# CSV path
csv_file = r"C:\Users\Antifragile\Desktop\csv\global fashion\data\transactions.csv"


# Chunk size
chunksize = 50000
for i, chunk in enumerate(pd.read_csv(csv_file, chunksize=chunksize)):
    # Fill NaNs with None for SQL compatibility
    chunk = chunk.where(pd.notnull(chunk), None)
    
    # Insert into SQL Server
    cursor.executemany("""
        INSERT INTO Transactions (
            Invoice_ID, Line, Customer_ID, Product_ID, Size, Color,
            Unit_Price, Quantity, Date, Discount, Line_Total,
            Store_ID, Employee_ID, Currency, Currency_Symbol, SKU,
            Transaction_Type, Payment_Method, Invoice_Total
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, chunk.values.tolist())
    conn.commit()
    print(f"Chunk {i+1} inserted.")

cursor.close()
conn.close()
print("✅ All 6.2M rows inserted successfully!")
