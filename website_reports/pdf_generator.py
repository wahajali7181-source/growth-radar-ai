from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


styles = getSampleStyleSheet()


def _add_heading(story, text):

    story.append(
        Paragraph(
            f"<b>{text}</b>",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 8))


def _add_list(story, items):

    if not items:

        story.append(
            Paragraph(
                "None",
                styles["BodyText"]
            )
        )

        story.append(Spacer(1, 8))

        return

    for item in items:

        story.append(

            Paragraph(

                f"• {item}",

                styles["BodyText"]

            )

        )

    story.append(Spacer(1, 8))


def generate_pdf(report, output_path):

    doc = SimpleDocTemplate(output_path)

    story = []

    story.append(

        Paragraph(

            "<b>Growth Radar AI</b>",

            styles["Title"]

        )

    )

    story.append(

        Paragraph(

            "Website Intelligence Report",

            styles["Heading1"]

        )

    )

    story.append(Spacer(1, 20))

    story.append(

        Paragraph(

            f"<b>Website:</b> {report['website']}",

            styles["BodyText"]

        )

    )

    story.append(

        Paragraph(

            f"<b>Date:</b> {report['generated_on']}",

            styles["BodyText"]

        )

    )

    story.append(Spacer(1, 20))

    _add_heading(story, "Overall Result")

    story.append(

        Paragraph(

            f"Overall Score : {report['overall_score']}/100",

            styles["BodyText"]

        )

    )

    story.append(

        Paragraph(

            f"Grade : {report['grade']}",

            styles["BodyText"]

        )

    )

    story.append(

        Paragraph(

            f"Priority : {report['priority']}",

            styles["BodyText"]

        )

    )

    story.append(Spacer(1, 20))

    _add_heading(story, "Scores")

    story.append(

        Paragraph(

            f"Health : {report['health_score']}%",

            styles["BodyText"]

        )

    )

    story.append(

        Paragraph(

            f"SEO : {report['seo_score']}%",

            styles["BodyText"]

        )

    )

    story.append(

        Paragraph(

            f"Security : {report['security_score']}%",

            styles["BodyText"]

        )

    )

    story.append(

        Paragraph(

            f"Performance : {report['performance_score']}%",

            styles["BodyText"]

        )

    )

    story.append(Spacer(1, 20))

    _add_heading(story, "Technology Stack")

    _add_list(

        story,

        report["technologies"]

    )

    _add_heading(story, "Executive Summary")

    story.append(

        Paragraph(

            report["summary"],

            styles["BodyText"]

        )

    )

    story.append(Spacer(1, 15))

    _add_heading(story, "Strengths")

    _add_list(

        story,

        report["strengths"]

    )

    _add_heading(story, "Weaknesses")

    _add_list(

        story,

        report["weaknesses"]

    )

    _add_heading(

        story,

        "Health Recommendations"

    )

    _add_list(

        story,

        report["health_recommendations"]

    )

    _add_heading(

        story,

        "SEO Recommendations"

    )

    _add_list(

        story,

        report["seo_recommendations"]

    )

    _add_heading(

        story,

        "Security Recommendations"

    )

    _add_list(

        story,

        report["security_recommendations"]

    )

    _add_heading(

        story,

        "Performance Recommendations"

    )

    _add_list(

        story,

        report["performance_recommendations"]

    )

    doc.build(story)

    return output_path