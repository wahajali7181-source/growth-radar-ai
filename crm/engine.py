import sqlite3
import pandas as pd

DB_NAME = "growthradar.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


# ======================================
# SAVE
# ======================================

def save_crm(
    business_id,
    starred,
    notes,
    followup_date,
    proposal_sent,
    status,
    estimated_value
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO crm(
            business_id,
            starred,
            notes,
            followup_date,
            proposal_sent,
            status,
            estimated_value
        )
        VALUES(?,?,?,?,?,?,?)
    """, (
        business_id,
        starred,
        notes,
        followup_date,
        proposal_sent,
        status,
        estimated_value
    ))

    conn.commit()
    conn.close()


# ======================================
# LOAD
# ======================================

def load_crm():

    conn = get_connection()

    df = pd.read_sql(
        "SELECT * FROM crm",
        conn
    )

    conn.close()

    return df


# ======================================
# GET SINGLE RECORD
# ======================================

def get_crm_by_id(business_id):

    conn = get_connection()

    query = """
        SELECT *
        FROM crm
        WHERE business_id = ?
    """

    df = pd.read_sql(
        query,
        conn,
        params=(business_id,)
    )

    conn.close()

    return df


# ======================================
# UPDATE
# ======================================

def update_crm(

    business_id,
    starred,
    notes,
    followup_date,
    proposal_sent,
    status,
    estimated_value

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        UPDATE crm

        SET

            starred=?,
            notes=?,
            followup_date=?,
            proposal_sent=?,
            status=?,
            estimated_value=?

        WHERE business_id=?

    """, (

        starred,
        notes,
        followup_date,
        proposal_sent,
        status,
        estimated_value,
        business_id

    ))

    conn.commit()
    conn.close()


# ======================================
# DELETE
# ======================================

def delete_crm(business_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM crm
        WHERE business_id=?
        """,
        (business_id,)
    )

    conn.commit()
    conn.close()