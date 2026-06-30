import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"))

    return connection


def save_detection(source_type, file_name, violations):
    conn = get_connection()
    cursor = conn.cursor()
    anomaly_status = True if violations else False

    # Insert metadata.
    cursor.execute(""" INSERT INTO detection_metadata
        (source_type,file_name,anomaly_status,total_violations)
             VALUES(%s,%s,%s,%s)RETURNING detection_id""",
                (source_type,file_name,anomaly_status,len(violations)))

    detection_id = cursor.fetchone()[0]

    # Insert each violation.
    for violation in violations:
        cursor.execute(""" INSERT INTO violation_details
            (detection_id,violation_type,confidence)
            VALUES(%s,%s,%s)""",
            ( detection_id,violation,0.0))

    conn.commit()

    cursor.close()
    conn.close()