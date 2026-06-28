from dataclasses import dataclass


@dataclass
class Business:

    name: str

    address: str = ""

    website: str = ""

    phone: str = ""

    email: str = ""

    rating: float = 0

    reviews: int = 0

    latitude: float = 0

    longitude: float = 0

    lead_score: int = 0

    opportunity: str = ""