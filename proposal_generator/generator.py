def generate_proposal(business, services, project_value):

    proposal = f"""
=============================
Growth Radar AI Proposal
=============================

Business:
{business['name']}

Lead Score:
{business['lead_score']}

Recommended Services:
"""

    for service in services:

        proposal += f"\n• {service}"

    proposal += f"""

Estimated Project Value:
${project_value}

Timeline:
30 Days

Expected Results:

• More Leads
• Better Online Presence
• Higher Google Visibility
• Increased Revenue

Prepared by:
Growth Radar AI
"""

    return proposal