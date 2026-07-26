import os


def create_project(

    business_name,
    app_code

):

    folder = f"generated_sites/{business_name}"

    os.makedirs(folder, exist_ok=True)

    src = os.path.join(folder, "src")

    os.makedirs(src, exist_ok=True)

    with open(

        os.path.join(src, "App.jsx"),

        "w",

        encoding="utf8"

    ) as f:

        f.write(app_code)

    return folder