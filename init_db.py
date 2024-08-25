import sqlite3


def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS participants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event TEXT NOT NULL,
        name TEXT NOT NULL,
        qr_code TEXT NOT NULL,
        UNIQUE(event, name)
    )
    """
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
