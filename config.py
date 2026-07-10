import os


class Config:

    # ================= SQL SERVER CONNECTION =================
    SQLALCHEMY_DATABASE_URI = (
        "mssql+pyodbc://@DESKTOP-OSR6ENO\\SQLEXPRESS/CRM_DB"
        "?driver=ODBC+Driver+18+for+SQL+Server"
        "&trusted_connection=yes"
        "&TrustServerCertificate=yes"
    )

    # ================= SQLALCHEMY SETTINGS =================
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ================= OPTIONAL SETTINGS =================
    SECRET_KEY = os.getenv(
        'SECRET_KEY',
        'crm-secret-key'
    )