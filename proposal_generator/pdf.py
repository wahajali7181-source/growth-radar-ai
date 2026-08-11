from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)
from reportlab.lib.units import inch


def generate_pdf(proposal):

    buffer = BytesIO()

    doc = SimpleDocTemplate(

        buffer,

        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,

    )

    styles = getSampleStyleSheet()

    title = styles["Title"]
    title.alignment = TA_CENTER
    title.textColor = colors.HexColor("#1E88E5")

    heading = styles["Heading2"]
    heading.textColor = colors.HexColor("#1565C0")

    body = styles["BodyText"]
    body.leading = 18

    footer = styles["Heading3"]
    footer.alignment = TA_CENTER
    footer.textColor = colors.grey

    story = []

    story.append(

        Paragraph(

            "Growth Radar AI",

            title,

        )

    )

    story.append(

        Paragraph(

            "Professional Business Growth Proposal",

            heading,

        )

    )

    story.append(

        Spacer(

            1,

            25,

        )

    )

    for line in proposal.split("\n"):

        text = line.strip()

        if not text:

            story.append(

                Spacer(

                    1,

                    8,

                )

            )

            continue

        if text.startswith("==="):

            continue

        if text.isupper():

            story.append(

                Spacer(

                    1,

                    8,

                )

            )

            story.append(

                Paragraph(

                    f"<b>{text}</b>",

                    heading,

                )

            )

            story.append(

                Spacer(

                    1,

                    6,

                )

            )

            continue

        story.append(

            Paragraph(

                text,

                body,

            )

        )

    story.append(

        Spacer(

            1,

            30,

        )

    )

    story.append(

        Paragraph(

            "Prepared by Growth Radar AI",

            footer,

        )

    )

    doc.build(story)

    buffer.seek(0)

    return buffer