from dataclasses import dataclass, asdict


@dataclass
class BusinessLead:

    name: str = ""

    business_type: str = ""

    city: str = ""

    address: str = ""

    website: str = ""

    phone: str = ""

    email: str = ""

    rating: float = 0.0

    reviews: int = 0

    facebook: str = ""

    instagram: str = ""

    linkedin: str = ""

    youtube: str = ""

    twitter: str = ""

    technology: str = ""

    seo_score: int = 0

    performance_score: int = 0

    security_score: int = 0

    website_health: int = 0

    lead_score: int = 0

    opportunity: str = ""

    ai_summary: str = ""

    source: str = ""

    place_id: str = ""

    latitude: float = 0.0

    longitude: float = 0.0

    def to_dict(self):

        return asdict(self) 
    