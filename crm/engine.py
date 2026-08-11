import sqlite3
import pandas as pd

from datetime import datetime

from auth.session import current_user


DB_NAME = "growthradar.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


# ==========================================
# CURRENT USER
# ==========================================

def _get_user_email():

    user = current_user()

    if not user:
        return None

    return user.get("email")


# ==========================================
# ENSURE CALL INTELLIGENCE COLUMNS
# ==========================================

def ensure_call_intelligence_columns():

    conn = get_connection()
    cursor = conn.cursor()

    columns = {

        "call_status": "TEXT DEFAULT ''",

        "call_outcome": "TEXT DEFAULT ''",

        "call_intent": "TEXT DEFAULT ''",

        "interest_level": "TEXT DEFAULT ''",

        "call_summary": "TEXT DEFAULT ''",

        "last_call_at": "TEXT DEFAULT ''",

        "callback_requested": "INTEGER DEFAULT 0",

    }

    cursor.execute(
        "PRAGMA table_info(crm)"
    )

    existing_columns = {

        row[1]

        for row in cursor.fetchall()

    }

    for column, definition in columns.items():

        if column not in existing_columns:

            cursor.execute(
                f"""
                ALTER TABLE crm
                ADD COLUMN {column} {definition}
                """
            )

    conn.commit()
    conn.close()


# ==========================================
# LOAD CRM
# ==========================================

def load_crm():

    ensure_call_intelligence_columns()

    user_email = _get_user_email()

    if not user_email:

        return pd.DataFrame()

    conn = get_connection()

    try:

        df = pd.read_sql(

            """
            SELECT *
            FROM crm
            WHERE user_email=?
            ORDER BY id DESC
            """,

            conn,

            params=(user_email,)

        )

    finally:

        conn.close()

    return df


# ==========================================
# GET SINGLE CRM RECORD
# ==========================================

def get_crm_by_id(business_id):

    ensure_call_intelligence_columns()

    user_email = _get_user_email()

    if not user_email:

        return pd.DataFrame()

    conn = get_connection()

    try:

        df = pd.read_sql(

            """
            SELECT *
            FROM crm
            WHERE business_id=?
            AND user_email=?
            """,

            conn,

            params=(

                business_id,
                user_email

            )

        )

    finally:

        conn.close()

    return df


# ==========================================
# SAVE / UPDATE CRM
# ==========================================

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
    deal_stage="Open",

    website="",
    location="",
    email="",
    phone="",
    lead_score=0

):

    ensure_call_intelligence_columns()

    user_email = _get_user_email()

    if not user_email:

        return False

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(

        """
        SELECT id
        FROM crm
        WHERE business_id=?
        AND user_email=?
        """,

        (

            business_id,

            user_email

        )

    )

    exists = cursor.fetchone()

    # ==========================================
    # UPDATE
    # ==========================================

    if exists:

        cursor.execute(

            """
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
                deal_stage=?,
                website=?,
                location=?,
                email=?,
                phone=?,
                lead_score=?

            WHERE business_id=?
            AND user_email=?
            """,

            (

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

                website,
                location,
                email,
                phone,
                lead_score,

                business_id,
                user_email

            )

        )

    # ==========================================
    # INSERT
    # ==========================================

    else:

        cursor.execute(

            """
            INSERT INTO crm(

                business_id,
                user_email,

                business_name,
                industry,
                website,
                location,
                email,
                phone,
                lead_score,

                status,
                priority,
                assigned_to,

                starred,
                proposal_sent,
                followup_date,
                meeting_date,

                notes,
                estimated_value,
                revenue,
                deal_stage

            )

            VALUES(

                ?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,?,?

            )
            """,

            (

                business_id,
                user_email,

                business_name,
                industry,
                website,
                location,
                email,
                phone,
                lead_score,

                status,
                priority,
                assigned_to,

                starred,
                proposal_sent,
                followup_date,
                meeting_date,

                notes,
                estimated_value,
                revenue,
                deal_stage

            )

        )

    conn.commit()
    conn.close()

    return True


# ==========================================
# LEGACY UPDATE FUNCTION
# ==========================================

def update_crm(

    business_id,
    starred,
    notes,
    followup_date,
    proposal_sent,
    status,
    estimated_value

):

    return save_crm(

        business_id,

        starred,

        notes,

        followup_date,

        proposal_sent,

        status,

        estimated_value

    )


# ==========================================
# DELETE CRM
# ==========================================

def delete_crm(business_id):

    user_email = _get_user_email()

    if not user_email:

        return False

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(

        """
        DELETE FROM crm

        WHERE business_id=?
        AND user_email=?
        """,

        (

            business_id,

            user_email

        )

    )

    conn.commit()
    conn.close()

    return True


# ==========================================
# MARK PROPOSAL AS SENT
# ==========================================

def mark_proposal_sent(business_id):

    user_email = _get_user_email()

    if not user_email:

        return False

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(

        """
        UPDATE crm

        SET proposal_sent=1

        WHERE business_id=?
        AND user_email=?
        """,

        (

            business_id,

            user_email

        )

    )

    conn.commit()

    updated = cursor.rowcount > 0

    conn.close()

    return updated


# ==========================================
# SAVE AI CALL RESULT
# ==========================================

def save_call_result(

    business_id,
    call_outcome="",
    call_intent="",
    interest_level="",
    call_summary="",
    callback_requested=False

):

    ensure_call_intelligence_columns()

    user_email = _get_user_email()

    if not user_email:

        return False

    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(

        """
        UPDATE crm

        SET

            call_status=?,
            call_outcome=?,
            call_intent=?,
            interest_level=?,
            call_summary=?,
            last_call_at=?,
            callback_requested=?

        WHERE business_id=?
        AND user_email=?

        """,

        (

            "Completed",

            call_outcome,

            call_intent,

            interest_level,

            call_summary,

            now,

            1 if callback_requested else 0,

            business_id,

            user_email

        )

    )

    updated = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return updated


# ==========================================
# GET CALL RESULT
# ==========================================

def get_call_result(business_id):

    ensure_call_intelligence_columns()

    user_email = _get_user_email()

    if not user_email:

        return None

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(

            """
            SELECT

                call_status,
                call_outcome,
                call_intent,
                interest_level,
                call_summary,
                last_call_at,
                callback_requested

            FROM crm

            WHERE business_id=?
            AND user_email=?

            """,

            (

                business_id,

                user_email

            )

        )

        return cursor.fetchone()

    finally:

        conn.close()