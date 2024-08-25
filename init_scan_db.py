import sqlite3


def init_scan_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event TEXT NOT NULL,
        name TEXT NOT NULL,
        scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(event, name)
    )
    """
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_scan_db()
