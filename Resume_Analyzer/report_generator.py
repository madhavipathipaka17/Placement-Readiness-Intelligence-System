# report_generator.py

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch


def generate_pdf_report(
        output_path,
        prediction,
        confidence,
        features,
        skill_gap,
        improvement_plan
):

    doc = SimpleDocTemplate(output_path)

    styles = getSampleStyleSheet()

    title = styles["Heading1"]
    title.alignment = TA_CENTER

    heading = styles["Heading2"]
    normal = styles["BodyText"]

    story = []

    # ---------------------------------------------------
    # Title
    # ---------------------------------------------------

    story.append(
        Paragraph(
            "Placement Readiness Intelligence Report",
            title
        )
    )

    story.append(Spacer(1, 0.3 * inch))

    # ---------------------------------------------------
    # Prediction
    # ---------------------------------------------------

    story.append(Paragraph("Prediction", heading))

    story.append(
        Paragraph(
            f"<b>Placement Readiness:</b> {prediction}",
            normal
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    # ---------------------------------------------------
    # Confidence Scores
    # ---------------------------------------------------

    story.append(
        Paragraph(
            "Confidence Scores",
            heading
        )
    )

    confidence_data = [["Category", "Probability (%)"]]

    for key, value in confidence.items():

        confidence_data.append([
            key,
            f"{round(value,2)}"
        ])

    confidence_table = Table(confidence_data)

    confidence_table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

            ("ALIGN", (0, 0), (-1, -1), "CENTER")

        ])

    )

    story.append(confidence_table)

    story.append(Spacer(1, 0.3 * inch))

    # ---------------------------------------------------
    # Features
    # ---------------------------------------------------

    story.append(
        Paragraph(
            "Extracted Features",
            heading
        )
    )

    feature_data = [["Feature", "Value"]]

    for column in features.columns:

        feature_data.append([
            column,
            str(features.iloc[0][column])
        ])

    feature_table = Table(feature_data)

    feature_table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke)

        ])

    )

    story.append(feature_table)

    story.append(Spacer(1, 0.3 * inch))

    # ---------------------------------------------------
    # Matched Skills
    # ---------------------------------------------------

    story.append(
        Paragraph(
            "Matched Skills",
            heading
        )
    )

    for skill in skill_gap["matched_skills"]:

        story.append(
            Paragraph(
                f"• {skill}",
                normal
            )
        )

    story.append(Spacer(1, 0.2 * inch))

    # ---------------------------------------------------
    # Missing Skills
    # ---------------------------------------------------

    story.append(
        Paragraph(
            "Missing Skills",
            heading
        )
    )

    for skill in skill_gap["missing_skills"]:

        story.append(
            Paragraph(
                f"• {skill}",
                normal
            )
        )

    story.append(Spacer(1, 0.2 * inch))

    # ---------------------------------------------------
    # Critical Missing Skills
    # ---------------------------------------------------

    story.append(
        Paragraph(
            "Critical Missing Skills",
            heading
        )
    )

    for skill in skill_gap["critical_missing_skills"]:

        story.append(
            Paragraph(
                f"• {skill}",
                normal
            )
        )

    story.append(Spacer(1, 0.2 * inch))

    # ---------------------------------------------------
    # Skills To Learn
    # ---------------------------------------------------

    story.append(
        Paragraph(
            "Skills To Learn First",
            heading
        )
    )

    for skill in skill_gap["skills_to_learn_first"]:

        story.append(
            Paragraph(
                f"• {skill}",
                normal
            )
        )

    story.append(Spacer(1, 0.3 * inch))

    # ---------------------------------------------------
    # Resume Suggestions
    # ---------------------------------------------------

    story.append(
        Paragraph(
            "Resume Improvement Suggestions",
            heading
        )
    )

    for suggestion in improvement_plan[
        "resume_improvement_suggestions"
    ]:

        story.append(
            Paragraph(
                f"• {suggestion}",
                normal
            )
        )

    story.append(Spacer(1, 0.2 * inch))

    # ---------------------------------------------------
    # Job Suggestions
    # ---------------------------------------------------

    story.append(
        Paragraph(
            "Job Preparation Suggestions",
            heading
        )
    )

    for suggestion in improvement_plan[
        "job_preparation_suggestions"
    ]:

        story.append(
            Paragraph(
                f"• {suggestion}",
                normal
            )
        )

    story.append(Spacer(1, 0.3 * inch))

    # ---------------------------------------------------
    # 7 Day Plan
    # ---------------------------------------------------

    story.append(
        Paragraph(
            "7-Day Improvement Plan",
            heading
        )
    )

    for day, tasks in improvement_plan[
        "seven_day_plan"
    ].items():

        story.append(
            Paragraph(
                f"<b>{day}</b>",
                normal
            )
        )

        for task in tasks:

            story.append(
                Paragraph(
                    f"• {task}",
                    normal
                )
            )

    story.append(Spacer(1, 0.3 * inch))

    # ---------------------------------------------------
    # 30 Day Plan
    # ---------------------------------------------------

    story.append(
        Paragraph(
            "30-Day Improvement Plan",
            heading
        )
    )

    for week, tasks in improvement_plan[
        "thirty_day_plan"
    ].items():

        story.append(
            Paragraph(
                f"<b>{week}</b>",
                normal
            )
        )

        for task in tasks:

            story.append(
                Paragraph(
                    f"• {task}",
                    normal
                )
            )

    story.append(Spacer(1, 0.3 * inch))

    # ---------------------------------------------------

    doc.build(story)

    return output_path