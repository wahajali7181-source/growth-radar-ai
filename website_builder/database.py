import os
import sqlite3
import uuid
from datetime import datetime


DATABASE_NAME = "growthradar.db"


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def get_connection():

    connection = sqlite3.connect(
        DATABASE_NAME,
        check_same_thread=False,
    )

    connection.row_factory = sqlite3.Row

    return connection


# ==========================================================
# CREATE WEBSITE REGISTRY TABLE
# ==========================================================

def create_websites_table():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS websites (

            id TEXT PRIMARY KEY,

            user_id INTEGER NOT NULL,

            business_name TEXT NOT NULL,

            business_type TEXT,

            folder_path TEXT NOT NULL,

            netlify_site_id TEXT,

            live_url TEXT,

            status TEXT NOT NULL DEFAULT 'generated',

            created_at TEXT NOT NULL,

            updated_at TEXT NOT NULL

        )
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_websites_user_id
        ON websites(user_id)
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_websites_status
        ON websites(status)
        """
    )

    connection.commit()

    connection.close()


# ==========================================================
# HELPERS
# ==========================================================

def _now():

    return datetime.utcnow().isoformat(
        timespec="seconds"
    )


def _row_to_dict(row):

    if row is None:

        return None

    return dict(row)


# ==========================================================
# CREATE WEBSITE RECORD
# ==========================================================

def create_website_record(
    user_id,
    business_name,
    business_type,
    folder_path,
    netlify_site_id=None,
    live_url=None,
    status="generated",
):

    if not user_id:

        return {

            "success": False,

            "message":
                "User ID is required."

        }

    if not business_name or not str(
        business_name
    ).strip():

        return {

            "success": False,

            "message":
                "Business name is required."

        }

    if not folder_path:

        return {

            "success": False,

            "message":
                "Website folder path is required."

        }

    website_id = str(
        uuid.uuid4()
    )

    timestamp = _now()

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO websites (

                id,
                user_id,
                business_name,
                business_type,
                folder_path,
                netlify_site_id,
                live_url,
                status,
                created_at,
                updated_at

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                website_id,
                user_id,
                str(
                    business_name
                ).strip(),
                str(
                    business_type or ""
                ).strip(),
                os.path.abspath(
                    folder_path
                ),
                netlify_site_id,
                live_url,
                status or "generated",
                timestamp,
                timestamp,
            ),
        )

        connection.commit()

        connection.close()

        return {

            "success": True,

            "website_id":
                website_id,

            "message":
                "Website record created successfully."

        }

    except Exception as e:

        return {

            "success": False,

            "message":
                "Unable to create website record.",

            "error":
                str(e)

        }


# ==========================================================
# GET USER WEBSITES
# ==========================================================

def get_user_websites(
    user_id
):

    if not user_id:

        return []

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM websites
            WHERE user_id = ?
            ORDER BY updated_at DESC
            """,
            (
                user_id,
            ),
        )

        rows = cursor.fetchall()

        connection.close()

        return [

            _row_to_dict(
                row
            )

            for row in rows

        ]

    except Exception:

        return []


# ==========================================================
# GET WEBSITE BY ID
# ==========================================================

def get_website_by_id(
    website_id,
    user_id,
):

    if not website_id:

        return None

    if not user_id:

        return None

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM websites
            WHERE id = ?
            AND user_id = ?
            LIMIT 1
            """,
            (
                website_id,
                user_id,
            ),
        )

        row = cursor.fetchone()

        connection.close()

        return _row_to_dict(
            row
        )

    except Exception:

        return None


# ==========================================================
# UPDATE WEBSITE RECORD
# ==========================================================

def update_website_record(
    website_id,
    user_id,
    **fields
):

    if not website_id:

        return {

            "success": False,

            "message":
                "Website ID is required."

        }

    if not user_id:

        return {

            "success": False,

            "message":
                "User ID is required."

        }

    allowed_fields = {

        "business_name",
        "business_type",
        "folder_path",
        "netlify_site_id",
        "live_url",
        "status",

    }

    updates = {

        key: value

        for key, value in fields.items()

        if key in allowed_fields

    }

    if not updates:

        return {

            "success": False,

            "message":
                "No valid website fields were provided."

        }

    if "folder_path" in updates:

        updates[
            "folder_path"
        ] = os.path.abspath(
            updates[
                "folder_path"
            ]
        )

    updates[
        "updated_at"
    ] = _now()

    try:

        connection = get_connection()

        cursor = connection.cursor()

        assignments = ", ".join(

            f"{field} = ?"

            for field in updates.keys()

        )

        values = list(
            updates.values()
        )

        query = f"""
            UPDATE websites
            SET {assignments}
            WHERE id = ?
            AND user_id = ?
        """

        values.extend(
            [
                website_id,
                user_id,
            ]
        )

        cursor.execute(
            query,
            values,
        )

        connection.commit()

        updated_rows = cursor.rowcount

        connection.close()

        if updated_rows < 1:

            return {

                "success": False,

                "message":
                    "Website record was not found or could not be updated."

            }

        return {

            "success": True,

            "message":
                "Website record updated successfully."

        }

    except Exception as e:

        return {

            "success": False,

            "message":
                "Unable to update website record.",

            "error":
                str(e)

        }


# ==========================================================
# DELETE WEBSITE RECORD
# ==========================================================

def delete_website_record(
    website_id,
    user_id,
):

    if not website_id:

        return {

            "success": False,

            "message":
                "Website ID is required."

        }

    if not user_id:

        return {

            "success": False,

            "message":
                "User ID is required."

        }

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM websites
            WHERE id = ?
            AND user_id = ?
            """,
            (
                website_id,
                user_id,
            ),
        )

        connection.commit()

        deleted_rows = cursor.rowcount

        connection.close()

        if deleted_rows < 1:

            return {

                "success": False,

                "message":
                    "Website record was not found."

            }

        return {

            "success": True,

            "message":
                "Website record deleted successfully."

        }

    except Exception as e:

        return {

            "success": False,

            "message":
                "Unable to delete website record.",

            "error":
                str(e)

        }