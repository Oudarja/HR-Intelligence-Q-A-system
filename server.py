# server.py
from fastapi import FastAPI
from fastmcp import FastMCP
import mysql.connector
import os
from dotenv import load_dotenv
from loguru import logger
import sys

# Configure loguru to show logs in console
# Remove default logger
logger.remove()  
# added logger for system output
logger.add(sys.stdout, level="DEBUG")  

load_dotenv()
User = os.getenv("MYSQL_USER", "root")
Password = os.getenv("MYSQL_PASSWORD", "")
DB_NAME = "hr_portal_db"  

mcp = FastMCP("MySQLAgent")
app = FastAPI()
app.mount('/',mcp.sse_app())

@mcp.tool()
def query_data(sql: str) -> str:
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user=User,
            password=Password,
            database="hr_portal_db"
        )
        cursor = conn.cursor()
        cursor.execute(sql)

        if sql.strip().lower().startswith("select"):
            result = cursor.fetchall()
            return "\n".join(str(row) for row in result) or "No data found."
        else:
            conn.commit()
            return "Query executed successfully."
    except Exception as e:
        logger.error(e)
        return f"Error: {str(e)}"
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass
