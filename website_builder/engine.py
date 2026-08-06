from website_builder.json_generator import generate_website_json
from website_builder.template_engine import build_react_template
from website_builder.project_builder import create_project


def generate_complete_website(

    business_name,
    business_type,
    audience,
    style,
    colors,
    pages,
    cta

):

    data = generate_website_json(

        business_name,

        business_type,

        audience,

        style,

        colors,

        pages,

        cta

    )

    if data is None:

        return None

    react_code = build_react_template(data)

    folder = create_project(

        business_name,

        react_code

    )

    return {

        "folder": folder,

        "react_code": react_code,

        "json": data

    }