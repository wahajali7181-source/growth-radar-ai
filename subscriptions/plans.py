PLANS = {

    "FREE": {

        "name": "Free",

        "price": 0,

        "monthly": False,

        "features": {

            "business_finder": 5,

            "website_scanner": 2,

            "crm_leads": 20,

            "proposal_writer": 5,

            "reports": 5,

            "ai_employees": False,

            "website_builder": False

        }

    },

    "STARTER": {

        "name": "Starter",

        "price": 19,

        "monthly": True,

        "features": {

            "business_finder": 100,

            "website_scanner": 50,

            "crm_leads": 500,

            "proposal_writer": 100,

            "reports": 100,

            "ai_employees": False,

            "website_builder": False

        }

    },

    "PROFESSIONAL": {

        "name": "Professional",

        "price": 49,

        "monthly": True,

        "features": {

            "business_finder": -1,

            "website_scanner": -1,

            "crm_leads": -1,

            "proposal_writer": -1,

            "reports": -1,

            "ai_employees": True,

            "website_builder": True

        }

    },

    "AGENCY": {

        "name": "Agency",

        "price": 99,

        "monthly": True,

        "features": {

            "business_finder": -1,

            "website_scanner": -1,

            "crm_leads": -1,

            "proposal_writer": -1,

            "reports": -1,

            "ai_employees": True,

            "website_builder": True,

            "team_members": True,

            "white_label": True,

            "api_access": True

        }

    }

}


def get_plan(plan_name):

    return PLANS.get(

        plan_name.upper(),

        PLANS["FREE"]

    )


def get_all_plans():

    return PLANS