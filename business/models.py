from dataclasses import dataclass, field


@dataclass
class Business:

    id: int | None = None

    name: str = ""

    website: str = ""

    phone: str = ""

    address: str = ""

    city: str = ""

    business_type: str = ""

    lead_score: int = 0

    opportunity: str = ""

    # CRM

    status: str = "New"

    priority: str = "Medium"

    assigned_to: str = ""

    proposal_sent: bool = False

    followup_date: str = ""

    meeting_date: str = ""

    notes: str = ""

    estimated_value: int = 0

    revenue: int = 0

    deal_stage: str = "Open"

    # Website

    seo_score: int = 0

    performance_score: int = 0

    security_score: int = 0

    accessibility_score: int = 0

    mobile_score: int = 0

    # AI

    ai_summary: str = ""

    recommendations: list = field(default_factory=list)