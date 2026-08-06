from ai.database import get_connection


def create_conversation(

    user_email,

    employee,

    title="New Chat"

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """

        INSERT INTO ai_conversations(

            user_email,

            employee,

            title

        )

        VALUES(?,?,?)

        """,

        (

            user_email,

            employee,

            title

        )

    )

    conn.commit()

    conversation_id = cursor.lastrowid

    conn.close()

    return conversation_id


def save_message(

    conversation_id,

    role,

    message

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """

        INSERT INTO ai_messages(

            conversation_id,

            role,

            message

        )

        VALUES(?,?,?)

        """,

        (

            conversation_id,

            role,

            message

        )

    )

    conn.commit()

    conn.close()


def load_messages(

    conversation_id

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT role,

               message

        FROM ai_messages

        WHERE conversation_id=?

        ORDER BY id ASC

        """,

        (

            conversation_id,

        )

    )

    rows = cursor.fetchall()

    conn.close()

    return rows