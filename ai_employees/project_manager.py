import streamlit as st
from ai_employees.ai_client import generate_response


def show():

    st.title("📋 AI Project Manager")

    st.caption(
        "Turn a client project into a structured execution plan "
        "with tasks, priorities, responsibilities and timelines."
    )

    st.divider()

    # ==========================================
    # PROJECT INFORMATION
    # ==========================================

    st.subheader("🏢 Project Information")

    col1, col2 = st.columns(2)

    with col1:

        business_name = st.text_input(
            "Business Name",
            placeholder="Example: Bright Dental Clinic",
            key="pm_business_name"
        )

        project_name = st.text_input(
            "Project Name",
            placeholder="Example: 90-Day Digital Growth Project",
            key="pm_project_name"
        )

        industry = st.text_input(
            "Industry",
            placeholder="Example: Dentist",
            key="pm_industry"
        )

    with col2:

        location = st.text_input(
            "Location",
            placeholder="Example: Lahore, Pakistan",
            key="pm_location"
        )

        budget = st.text_input(
            "Project Budget",
            placeholder="Example: $1,000/month",
            key="pm_budget"
        )

        timeline = st.selectbox(
            "Project Timeline",
            [
                "7 Days",
                "14 Days",
                "30 Days",
                "60 Days",
                "90 Days",
                "Custom"
            ],
            key="pm_timeline"
        )

    st.divider()

    # ==========================================
    # PROJECT GOAL
    # ==========================================

    st.subheader("🎯 Project Goal")

    project_goal = st.text_area(
        "What should this project achieve?",
        placeholder=(
            "Example: Generate more local dental leads, "
            "improve Google visibility and increase appointments."
        ),
        height=120,
        key="pm_goal"
    )

    services = st.multiselect(
        "Services Involved",
        [
            "Business Audit",
            "SEO",
            "Local SEO",
            "Google Ads",
            "Meta Ads",
            "Social Media Management",
            "Content Creation",
            "Video Editing",
            "Graphic Designing",
            "Website Development",
            "Website Optimization",
            "Lead Generation",
            "CRM",
            "Reporting"
        ],
        key="pm_services"
    )

    team_members = st.text_area(
        "Available Team Members",
        placeholder=(
            "Example:\n"
            "SEO Expert\n"
            "Creative Director\n"
            "Social Media Manager\n"
            "Copywriter"
        ),
        height=120,
        key="pm_team"
    )

    additional_information = st.text_area(
        "Additional Project Information",
        placeholder=(
            "Client requirements, deadlines, special instructions, "
            "deliverables or anything else the project manager should know."
        ),
        height=120,
        key="pm_extra"
    )

    st.divider()

    # ==========================================
    # GENERATE PROJECT PLAN
    # ==========================================

    if st.button(
        "🚀 Create Project Execution Plan",
        use_container_width=True,
        key="pm_generate"
    ):

        if not business_name.strip():

            st.warning("Please enter the Business Name.")
            return

        if not project_name.strip():

            st.warning("Please enter the Project Name.")
            return

        if not project_goal.strip():

            st.warning("Please describe the Project Goal.")
            return

        service_text = (
            ", ".join(services)
            if services
            else "Not provided"
        )

        team_text = (
            team_members
            if team_members.strip()
            else "Not provided"
        )

        extra_text = (
            additional_information
            if additional_information.strip()
            else "Not provided"
        )

        # ======================================
        # SYSTEM PROMPT
        # ======================================

        system_prompt = """
You are an elite international Project Manager working
inside Growth Radar AI.

Your job is to convert a client project into a realistic,
structured and executable project management plan.

Think like a senior agency project manager.

QUALITY RULES:

1. Use ONLY information supplied by the user.

2. NEVER invent:
- team members
- completed tasks
- deadlines already achieved
- client approvals
- project results
- budgets
- performance data

3. If information is unavailable, clearly label it:
- Recommended
- To be confirmed
- To be assigned
- To be reviewed

4. Create practical tasks that a real agency team can execute.

5. Every major task should include:
WHAT
WHO
WHEN
PRIORITY
DEPENDENCY
DELIVERABLE

6. Prioritize tasks logically.

7. Identify project risks and blockers.

8. Create realistic phases.

9. Focus on business outcomes.

10. Do not guarantee business results.

11. Never mention internal AI implementation,
API limitations, credits or demo mode.

12. Return ONLY clean Markdown.

13. Do not wrap the complete response inside
```markdown
```.
"""

        # ======================================
        # USER PROMPT
        # ======================================

        user_prompt = f"""
Create a complete project execution plan.

==================================================
PROJECT INFORMATION
==================================================

Business Name:
{business_name}

Project Name:
{project_name}

Industry:
{industry if industry.strip() else "Not provided"}

Location:
{location if location.strip() else "Not provided"}

Budget:
{budget if budget.strip() else "Not provided"}

Timeline:
{timeline}

Project Goal:
{project_goal}

Services:
{service_text}

Available Team:
{team_text}

Additional Information:
{extra_text}


==================================================
CREATE THIS PROJECT MANAGEMENT REPORT
==================================================

# 1. Project Executive Summary

Explain:

- Project objective
- Main business outcome
- Project scope
- Overall execution direction


# 2. Project Scope

Separate:

## In Scope

## Out of Scope

Do not invent information.


# 3. Project Phases

Create logical project phases.

For each phase explain:

- Objective
- Tasks
- Deliverables
- Dependencies


# 4. Task Breakdown

Create a detailed task table containing:

| Task | Responsible Employee | Priority | Timeline | Dependency | Deliverable |

Use available team members where provided.

If no team member is available, write:

"To be assigned"


# 5. Timeline

Create a realistic timeline based on the supplied project duration.

Break it into:

- Day/Week
- Tasks
- Owner
- Deliverable


# 6. Employee Responsibilities

Clearly explain what each available employee should handle.

For example:

SEO Expert
Creative Director
Social Media Manager
Copywriter

Only include employees actually provided or logically required.


# 7. Dependencies

Identify tasks that must happen before other tasks.

Example:

Business Audit
→ Strategy
→ Content/Creative
→ Campaign Launch
→ Optimization
→ Reporting


# 8. Priority Matrix

Classify tasks as:

🔴 Critical
🟠 High
🟡 Medium
🟢 Low

Explain why each critical/high task matters.


# 9. Project Risks

Identify realistic risks such as:

- Missing client information
- Delayed approvals
- Missing website access
- Missing ad account access
- Delayed creative approval
- Unclear requirements
- Resource constraints

Do not claim that these risks currently exist.
Present them as potential risks to monitor.


# 10. Client Requirements

List information/access/assets that should be requested from the client.


# 11. Weekly Project Management Plan

Create a week-by-week management checklist covering:

- Task tracking
- Team coordination
- Client communication
- Approvals
- Quality control
- Progress review


# 12. Quality Control Checklist

Create checks for:

- Strategy quality
- Content quality
- Creative quality
- Technical implementation
- Client requirements
- Deliverables


# 13. Project Status Dashboard

Create a recommended dashboard structure:

- Overall Status
- Completed Tasks
- Pending Tasks
- Blocked Tasks
- Upcoming Tasks
- Critical Risks
- Client Approvals


# 14. Final Project Manager Recommendation

Provide:

- First 3 actions
- Most important dependency
- Biggest potential blocker
- Highest priority deliverable
- Recommended next step

Be practical and specific.

Explain:

WHAT → WHO → WHEN → WHY
"""

        # ======================================
        # AI GENERATION
        # ======================================

        with st.spinner(
            "🤖 AI Project Manager is building the execution plan..."
        ):

            result = generate_response(
                prompt=user_prompt,
                system_prompt=system_prompt
            )

        # ======================================
        # HANDLE RESULT
        # ======================================

        if result:

            st.session_state[
                "project_manager_result"
            ] = result

            st.session_state[
                "project_manager_business"
            ] = business_name

            st.success(
                "✅ Project Execution Plan Generated."
            )

        else:

            st.error(
                "❌ Unable to generate project plan."
            )

    # ==========================================
    # DISPLAY RESULT
    # ==========================================

    result = st.session_state.get(
        "project_manager_result"
    )

    result_business = st.session_state.get(
        "project_manager_business",
        business_name
        if "business_name" in locals()
        else ""
    )

    if result:

        st.divider()

        st.subheader(
            f"📋 Project Plan — {result_business}"
        )

        st.markdown(result)

        st.divider()

        st.download_button(
            "📥 Download Project Plan",
            data=result,
            file_name=(
                f"{result_business}_project_plan.md"
            ),
            mime="text/markdown",
            use_container_width=True
        )