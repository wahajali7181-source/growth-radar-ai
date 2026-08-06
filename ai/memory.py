from services.context_service import get_context


def build_memory():

    context = get_context()

    return {

        "businesses": context.get(

            "businesses",

            []

        ),

        "crm": context.get(

            "crm",

            []

        )

    }