import pyodbc


try:

    conn = pyodbc.connect(

        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=DESKTOP-OSR6ENO\\SQLEXPRESS;"
        "DATABASE=CRM_DB;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

    print("✅ Connected successfully!")

    cursor = conn.cursor()

    cursor.execute("SELECT DB_NAME()")

    database_name = cursor.fetchone()[0]

    print(f"✅ Connected Database: {database_name}")

    conn.close()

except Exception as e:

    print("❌ Connection Failed")

    print(e)