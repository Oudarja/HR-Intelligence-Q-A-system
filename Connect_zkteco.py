from zk import ZK, const
import mysql.connector
import os
from dotenv import load_dotenv
from loguru import logger
import sys
conn = None

# Create ZK instance
# force_udp=False
#The library will use TCP to connect to the ZKTeco device.

# This line creates an instance of the ZK class, which is the main entry point for communicating with a ZKTeco device.
# Timeout (5):The maximum time (in seconds) that the library waits for a response from the device before raising an error.
# force_udp (False):Determines whether to use the UDP protocol or TCP. Setting it to False uses TCP. (The choice can affect
#  reliability and buffer handling.)

# ommit_ping (optional, not shown here):
# When true, the library skips sending a preliminary ping to the device. (In some versions this parameter is available to
#  disable ICMP checks.)

zk = ZK('172.16.2.155', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=True)

try:
    # Connect to device
    # Establishes a communication session with the device.
    conn = zk.connect()
    print("✅ Connected to the device")

    # Configure loguru to show logs in console
    # # Remove default logger
    logger.remove()  
    # added logger for system output
    logger.add(sys.stdout, level="DEBUG")  

    load_dotenv()
    User = os.getenv("MYSQL_USER", "root")
    Password = os.getenv("MYSQL_PASSWORD", "")
    DB_NAME = "hr_portal_db"  

    conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user=User,
            password=Password,
            database="hr_portal_db"
    )

    # Disable device to safely perform operations
    # Disabling prevents the device from updating its state (e.g., processing new finger scans or clock-ins)
    # during operations, ensuring data consistency.
    conn.disable_device()

    # -----------------------------
    # Get All Users
    # -----------------------------
    print("\n👤 Enrolled Users:")
    # Retrieves a list of all registered/enrolled users on the device.
    users = conn.get_users()

    for user in users:
        privilege = 'User'
        if user.privilege == const.USER_ADMIN:
            privilege = 'Admin'
        
        # print('+ UID #{}'.format(user.uid))
        # print('  Name       : {}'.format(user.name))
        # print('  Privilege  : {}'.format(privilege))
        # print('  Password   : {}'.format(user.password))
        # print('  Group ID   : {}'.format(user.group_id))
        # print('  User  ID   : {}'.format(user.user_id))

    # -----------------------------
    # Get Attendance Logs
    # -----------------------------
    print("\n📥 Attendance Logs:")
    # Fetches the attendance logs stored on the device.
    attendance = conn.get_attendance()

    # Connect to MySQL
    conn = mysql.connector.connect(
    host='localhost',
    user='your_user',
    password='your_password',
    database='your_database'
    )
    cursor = conn.cursor()
    # Assume `user` is from the device and `privilege` is determined
    sql = """
    INSERT INTO employee (uid, name, privilege, password, group_id, user_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    val = (
        user.uid,
    user.name,
    privilege,  # Already mapped: 'User' or 'Admin'
    user.password,
    user.group_id,
    user.user_id
    )
    cursor.execute(sql, val)
    conn.commit()

    # for log in attendance:
    #     print("  User ID: {:<10} Time: {} Status: {}".format(log.user_id, log.timestamp, log.status))

    # Optional: Test voice (Thank you)
    # This function is used to trigger a voice prompt or audible confirmation from the device.
    conn.test_voice()

    # Re-enable device
    # It is important to re-enable the device so that it 
    # resumes normal operation (allowing new clock-ins or fingerprint inputs).
    conn.enable_device()

except Exception as e:
    print("❌ Process terminated: {}".format(e))

finally:
    if conn:
        conn.disconnect()
        print("🔌 Disconnected from device")
