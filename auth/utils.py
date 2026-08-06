import bcrypt
import re


# ==========================================
# HASH PASSWORD
# ==========================================

def hash_password(password):

    password = password.encode("utf-8")

    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(

        password,

        salt

    )

    return hashed.decode("utf-8")


# ==========================================
# VERIFY PASSWORD
# ==========================================

def verify_password(

    password,

    hashed_password

):

    return bcrypt.checkpw(

        password.encode("utf-8"),

        hashed_password.encode("utf-8")

    )


# ==========================================
# EMAIL VALIDATION
# ==========================================

def is_valid_email(email):

    pattern = (

        r"^[A-Za-z0-9._%+-]+"

        r"@[A-Za-z0-9.-]+"

        r"\.[A-Za-z]{2,}$"

    )

    return re.match(

        pattern,

        email

    ) is not None


# ==========================================
# PASSWORD STRENGTH
# ==========================================

def password_strength(password):

    if len(password) < 8:

        return False, "Password must be at least 8 characters."

    if not re.search(r"[A-Z]", password):

        return False, "Password must contain an uppercase letter."

    if not re.search(r"[a-z]", password):

        return False, "Password must contain a lowercase letter."

    if not re.search(r"[0-9]", password):

        return False, "Password must contain a number."

    return True, "Strong Password"