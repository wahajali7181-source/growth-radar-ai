from dataclasses import dataclass


@dataclass
class Business:

    name: str = ""

    address: str = ""

    latitude: str = ""

    longitude: str = ""

    website: str = ""

    phone: str = ""

    email: str = ""

    instagram: str = ""

    facebook: str = ""

    linkedin: str = ""

    rating: float | None = None

    reviews: int | None = None

    lead_score: int = 0

    opportunity: str = ""