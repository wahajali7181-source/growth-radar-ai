from database.database import database

database.save_audit(

    "PureGym",

    "https://puregym.com",

    84,

    "Good"

)

rows = database.get_all_audits()

print()

for row in rows:

    print(row)