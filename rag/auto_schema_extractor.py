import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def extract_mysql_schema():

    """_summary_: extracts MySQL table schema → saves it in rag/db_schema.md
    """    
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE","hr_portal_db")
    )
    cursor = conn.cursor()

    schema = ""
    cursor.execute("SHOW TABLES")
    for (table_name,) in cursor.fetchall():
        schema += f"### Table: {table_name}\n"
        cursor.execute(f"DESCRIBE {table_name}")
        for row in cursor.fetchall():
            col_name, col_type = row[0], row[1]
            schema += f"- {col_name}: {col_type}\n"
        schema += "\n"

    cursor.close()
    conn.close()

    with open("rag/db_schema.md", "w") as f:
        f.write(schema)

    print("[✅] Schema extracted and saved to rag/db_schema.md")
