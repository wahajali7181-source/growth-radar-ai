from datetime import datetime


def generate_proposal(

    business,
    services,
    project_value,

):

    business_name = business.get("name", "Unknown Business")

    lead_score = business.get("lead_score", "N/A")

    website = business.get("website", "Not Available")

    email = business.get("email", "Not Available")

    phone = business.get("phone", "Not Available")

    proposal = f"""
==========================================================
                 GROWTH RADAR AI
           AI BUSINESS GROWTH PROPOSAL
==========================================================

Proposal Date
----------------------------------------
{datetime.now().strftime("%d %B %Y")}

Business Information
----------------------------------------
Business Name : {business_name}

Website       : {website}

Email         : {email}

Phone         : {phone}

Lead Score    : {lead_score}/100

==========================================================
PROJECT OBJECTIVE
==========================================================

Our objective is to increase your online visibility,
generate qualified leads, improve conversion rates,
and build a scalable digital growth system.

==========================================================
RECOMMENDED SERVICES
==========================================================
"""

    for index, service in enumerate(services, start=1):

        proposal += f"{index}. {service}\n"

    proposal += f"""

==========================================================
EXPECTED RESULTS
==========================================================

✓ More Qualified Leads

✓ Higher Search Visibility

✓ Better Brand Authority

✓ Better Customer Trust

✓ Increased Conversion Rate

✓ Long-Term Digital Growth

==========================================================
PROJECT TIMELINE
==========================================================

Week 1
-------
Business Audit
Strategy Planning

Week 2
-------
Implementation

Week 3
-------
Optimization

Week 4
-------
Reporting
Scaling

==========================================================
PROJECT INVESTMENT
==========================================================

Estimated Value

${project_value}

==========================================================
WHY GROWTH RADAR AI
==========================================================

• AI Powered Analysis

• Professional Proposal Generation

• Business Intelligence

• CRM Integration

• Website Intelligence

• Growth Recommendations

==========================================================
Prepared By

Growth Radar AI

==========================================================
"""

    return proposal