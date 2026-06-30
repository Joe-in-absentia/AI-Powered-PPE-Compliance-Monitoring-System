import os
import pandas as pd
import yagmail
from dotenv import load_dotenv
from database import get_connection

load_dotenv()

def generate_csv():
    conn = get_connection()
    query = """ SELECT m.timestamp,m.source_type,m.file_name,m.anomaly_status,
                   m.total_violations,v.violation_type,v.confidence
                FROM detection_metadata m
                JOIN violation_details v ON m.detection_id = v.detection_id
                ORDER BY m.timestamp DESC """

    df = pd.read_sql(query, conn)
    file_name = "IntelliGuard_violation_report.csv"

    df.to_csv( file_name,index=False)

    conn.close()
    return file_name

def send_report():
    csv_file = generate_csv()

    gmail = yagmail.SMTP(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))
    gmail.send(to=os.getenv("RECEIVER_EMAIL"), subject="IntelliGuard PRO Violation Report",
        contents=""" IntelliGuard PRO
        Attached is the latest violation report. """,attachments=csv_file)
    
