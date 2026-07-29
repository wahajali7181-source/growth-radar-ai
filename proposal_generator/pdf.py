from io import BytesIO

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)


def generate_pdf(proposal):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(

        Paragraph(

            "<b><font size=22>Growth Radar AI</font></b>",

            styles["Title"]

        )

    )

    story.append(

        Paragraph(

            "Professional Business Proposal",

            styles["Heading2"]

        )

    )

    story.append(Spacer(1, 20))

    for line in proposal.split("\n"):

        if line.strip() == "":

            story.append(Spacer(1, 8))

        else:

            story.append(

                Paragraph(

                    line,

                    styles["BodyText"]

                )

            )

    story.append(Spacer(1, 20))

    story.append(

        Paragraph(

            "<b>Prepared by Growth Radar AI</b>",

            styles["Heading3"]

        )

    )

    doc.build(story)

    buffer.seek(0)

    return buffer