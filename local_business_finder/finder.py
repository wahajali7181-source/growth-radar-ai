import pandas as pd


def find_businesses(
    business_type,
    city
):

    data = [
        {
            "name": f"{business_type} One",
            "city": city,
            "rating": 4.5
        },
        {
            "name": f"{business_type} Plus",
            "city": city,
            "rating": 4.2
        },
        {
            "name": f"{business_type} Expert",
            "city": city,
            "rating": 4.8
        }
    ]

    return pd.DataFrame(data)