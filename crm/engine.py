import sqlite3
import pandas as pd

DB_NAME = "growthradar.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


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
# SAVE / UPDATE
# ======================================

def save_crm(

    business_id,
    starred,
    notes,
    followup_date,
    proposal_sent,
    status,
    estimated_value,

    business_name="",
    industry="",
    priority="Medium",
    assigned_to="",
    meeting_date="",
    revenue=0,
    deal_stage="Open"

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT id

    FROM crm

    WHERE business_id=?

    """, (business_id,))

    exists = cursor.fetchone()

    if exists:

        cursor.execute("""

        UPDATE crm

        SET

        starred=?,
        notes=?,
        followup_date=?,
        proposal_sent=?,
        status=?,
        estimated_value=?,
        business_name=?,
        industry=?,
        priority=?,
        assigned_to=?,
        meeting_date=?,
        revenue=?,
        deal_stage=?

        WHERE business_id=?

        """, (

            starred,
            notes,
            followup_date,
            proposal_sent,
            status,
            estimated_value,

            business_name,
            industry,
            priority,
            assigned_to,
            meeting_date,
            revenue,
            deal_stage,

            business_id

        ))

    else:

        cursor.execute("""

        INSERT INTO crm(

        business_id,
        starred,
        notes,
        followup_date,
        proposal_sent,
        status,
        estimated_value,

        business_name,
        industry,
        priority,
        assigned_to,
        meeting_date,
        revenue,
        deal_stage

        )

        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)

        """, (

            business_id,
            starred,
            notes,
            followup_date,
            proposal_sent,
            status,
            estimated_value,

            business_name,
            industry,
            priority,
            assigned_to,
            meeting_date,
            revenue,
            deal_stage

        ))

    conn.commit()
    conn.close()


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

    save_crm(

        business_id,

        starred,

        notes,

        followup_date,

        proposal_sent,

        status,

        estimated_value

    )


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