import sqlite3
from datetime import datetime


DATABASE_FILE = "security_events.db"


def get_connection():
    return sqlite3.connect(DATABASE_FILE)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS security_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            event_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            message TEXT,
            port INTEGER,
            address TEXT,
            pid TEXT,
            process TEXT
        )
    """)

    connection.commit()
    connection.close()


def log_event(
    event_type,
    severity,
    message,
    port=None,
    address=None,
    pid=None,
    process=None
):
    connection = get_connection()
    cursor = connection.cursor()

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO security_events
        (
            timestamp,
            event_type,
            severity,
            message,
            port,
            address,
            pid,
            process
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        event_type,
        severity,
        message,
        port,
        address,
        pid,
        process
    ))

    connection.commit()
    connection.close()


def get_recent_events(limit=20):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            timestamp,
            event_type,
            severity,
            message,
            port,
            address,
            pid,
            process
        FROM security_events
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    events = cursor.fetchall()

    connection.close()

    return events


if __name__ == "__main__":
    initialize_database()
    print("[+] Security database initialized.")