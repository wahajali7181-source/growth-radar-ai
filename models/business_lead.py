from dataclasses import dataclass, field


@dataclass
class BusinessLead:

    # ==========================
    # Basic Information
    # ==========================

    name: str = ""

    category: str = ""

    city: str = ""

    address: str = ""

    latitude: float = 0.0

    longitude: float = 0.0

    # ==========================
    # Contact
    # ==========================

    website: str = ""

    email: str = ""

    phone: str = ""

    # ==========================
    # Social
    # ==========================

    facebook: str = ""

    instagram: str = ""

    linkedin: str = ""

    youtube: str = ""

    # ==========================
    # Reputation
    # ==========================

    rating: float = 0.0

    reviews: int = 0

    # ==========================
    # Lead Engine
    # ==========================

    lead_score: int = 0

    opportunity: str = ""

    # ==========================
    # Website Analysis
    # ==========================

    website_status: str = ""

    seo_score: int = 0

    security_score: int = 0

    performance_score: int = 0

    # ==========================
    # AI
    # ==========================

    ai_summary: str = ""

    ai_actions: list = field(default_factory=list)

    # ==========================
    # Future AI Employees
    # ==========================

    proposal: str = ""

    outreach_email: str = ""

    ad_strategy: str = ""

    website_plan: str = ""

    social_strategy: str = ""

    sales_status: str = ""