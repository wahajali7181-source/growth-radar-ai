import sqlite3


class Database:

    def __init__(self):

        self.connection = sqlite3.connect(
            "database/growthradar.db",
            check_same_thread=False
        )

        self.cursor = self.connection.cursor()

        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS audits(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            business_name TEXT,

            website TEXT,

            score INTEGER,

            priority TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

        """)

        self.connection.commit()

    def save_audit(

        self,

        business_name,

        website,

        score,

        priority

    ):

        self.cursor.execute("""

        INSERT INTO audits(

            business_name,

            website,

            score,

            priority

        )

        VALUES(?,?,?,?)

        """,(

            business_name,

            website,

            score,

            priority

        ))

        self.connection.commit()

    def get_all_audits(self):

        self.cursor.execute("""

        SELECT *

        FROM audits

        ORDER BY id DESC

        """)

        return self.cursor.fetchall()


database = Database()