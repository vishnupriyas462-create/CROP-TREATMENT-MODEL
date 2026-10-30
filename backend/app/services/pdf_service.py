"""
PDF Report Generation Service for AgriGuard AI.
Uses ReportLab to generate official-looking, printable crop diagnostic reports.
"""

import io
from typing import Dict, Any
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether
)


def generate_crop_health_pdf(data: Dict[str, Any]) -> bytes:
    """Generates a structured PDF document for a given analysis record."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#14532d")
    )
    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#475569")
    )
    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#166534"),
        spaceBefore=10,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1e293b")
    )
    bullet_style = ParagraphStyle(
        "BulletText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155")
    )
    disclaimer_style = ParagraphStyle(
        "Disclaimer",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#64748b")
    )

    story = []

    # 1. Header Banner
    story.append(Paragraph("AgriGuard AI — Smart Crop Health Diagnosis", title_style))
    story.append(Paragraph("AI-Powered Agricultural Decision Support & Integrated Pest Management Report", subtitle_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#16a34a"), spaceAfter=12))

    # 2. Metadata Table
    meta_data = [
        [
            Paragraph(f"<b>Analysis ID:</b> {data.get('id', 'N/A')}", body_style),
            Paragraph(f"<b>Date/Time:</b> {data.get('timestamp', 'N/A')}", body_style)
        ],
        [
            Paragraph(f"<b>Crop:</b> {data.get('crop_name', 'Unknown')}", body_style),
            Paragraph(f"<b>Growth Stage:</b> {data.get('growth_stage') or 'Vegetative'}", body_style)
        ],
        [
            Paragraph(f"<b>Location/District:</b> {data.get('district') or 'Unspecified'}", body_style),
            Paragraph(f"<b>Confidence:</b> {data.get('confidence', 0):.1f}%", body_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[270, 270])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#e2e8f0")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#f1f5f9")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # 3. Diagnosis Banner
    disease_name = data.get("disease_name", "Unknown")
    is_healthy = data.get("is_healthy", False)
    status_bg = colors.HexColor("#dcfce7") if is_healthy else colors.HexColor("#fee2e2")
    status_text_color = "#15803d" if is_healthy else "#991b1b"

    diag_text = f"<b>Predicted Diagnosis:</b> {disease_name} &nbsp;|&nbsp; <b>Category:</b> {data.get('disease_type', 'N/A').title()}"
    diag_p = Paragraph(f"<font color='{status_text_color}'>{diag_text}</font>", ParagraphStyle(
        "DiagP", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=10.5, leading=14
    ))
    diag_table = Table([[diag_p]], colWidths=[540])
    diag_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), status_bg),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(diag_table)
    story.append(Spacer(1, 10))

    # 4. Symptoms and Spread
    story.append(Paragraph("1. Symptoms & Environmental Conditions", heading_style))
    story.append(Paragraph(data.get("symptoms_summary") or "Foliar assessment indicates localized tissue changes.", bullet_style))
    story.append(Spacer(1, 8))

    # 5. Immediate Next Steps & Prevention
    story.append(Paragraph("2. Recommended Field Actions & Farm Hygiene", heading_style))
    notes = data.get("notes") or "Scout field twice weekly. Isolate infected specimens and prevent splashing irrigation water."
    story.append(Paragraph(f"• {notes}", bullet_style))
    story.append(Spacer(1, 8))

    # 5b. Dedicated Step-by-Step Action Plan
    action_plan = data.get("action_plan")
    if action_plan:
        story.append(Paragraph(f"<b>ACTION PLAN — {action_plan.get('urgency', 'Immediate Guidelines')}</b>", heading_style))
        plan_rows = [
            [Paragraph("<b>Step 1: Immediate Field Action</b>", body_style), Paragraph(action_plan.get("step_1_immediate", ""), bullet_style)],
            [Paragraph("<b>Step 2: Biological & Cultural Control</b>", body_style), Paragraph(action_plan.get("step_2_biological_cultural", ""), bullet_style)],
            [Paragraph("<b>Step 3: Chemical Spray (If Needed)</b>", body_style), Paragraph(action_plan.get("step_3_chemical_application", ""), bullet_style)],
            [Paragraph("<b>Step 4: Day 7 Monitoring</b>", body_style), Paragraph(action_plan.get("step_4_monitoring", ""), bullet_style)]
        ]
        plan_table = Table(plan_rows, colWidths=[160, 380])
        plan_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f0fdf4")),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#86efac")),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#dcfce7")),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(plan_table)
        story.append(Spacer(1, 8))

        # Critical Do-Nots
        donots = action_plan.get("critical_donots", [])
        if donots:
            story.append(Paragraph("<b>Critical Mistakes to Avoid:</b>", ParagraphStyle(
                "DonotHeading", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=9, textColor=colors.HexColor("#991b1b")
            )))
            for dn in donots:
                story.append(Paragraph(f"• <font color='#991b1b'>{dn}</font>", bullet_style))
            story.append(Spacer(1, 8))

    # 6. Verified Treatment Guidance
    guidance_list = data.get("guidance", [])
    story.append(Paragraph("3. Verified Agricultural Guidance & Integrated Pest Management", heading_style))

    if guidance_list:
        for item in guidance_list:
            card_data = [
                [Paragraph(f"<b>Category:</b> {item.get('treatment_category', 'N/A').upper()} &nbsp;|&nbsp; <b>Product / Active:</b> {item.get('approved_product_name') or item.get('active_ingredient', 'N/A')}", body_style)],
                [Paragraph(f"<b>Dosage / Application:</b> {item.get('dosage_guidance', 'Refer to certified product label')}", bullet_style)],
                [Paragraph(f"<b>Non-Chemical / IPM Alternative:</b> {item.get('non_chemical_control', 'N/A')}", bullet_style)],
                [Paragraph(f"<b>Safety Precautions:</b> {item.get('safety_precautions', 'Wear protective equipment (gloves, mask).')}", bullet_style)],
                [Paragraph(f"<b>Official Source Citation:</b> {item.get('source_org', 'N/A')} - {item.get('reference_citation', '')} (Verified: {item.get('verification_date', '')})", disclaimer_style)]
            ]
            t = Table(card_data, colWidths=[540])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
                ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(t)
            story.append(Spacer(1, 6))
    else:
        story.append(Paragraph("No chemical treatment recommendation is applicable for healthy crops or unverified pathogens. Maintain preventive cultural practices and consult local KVK specialists.", bullet_style))
        story.append(Spacer(1, 6))

    # 7. Official Advisory Helpline
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Agricultural Extension Helpline:</b> Kisan Call Center: <b>1800-180-1551</b> (Toll-Free, 22 Languages) | TNAU Agritech: <b>0422-6611383</b>", body_style))
    story.append(Spacer(1, 10))

    # 8. Disclaimer
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=6))
    disclaimer_text = (
        "<b>Important Safety Disclaimer:</b> AgriGuard AI is an educational decision-support tool powered by machine learning. "
        "Confidence scores reflect statistical model similarity, not a certified agronomic diagnosis. Always confirm disease identification "
        "with an accredited agricultural extension officer or Krishi Vigyan Kendra before purchasing or applying registered crop protection chemicals. "
        "Strictly adhere to manufacturer label safety instructions, protective equipment requirements, and harvest waiting periods."
    )
    story.append(Paragraph(disclaimer_text, disclaimer_style))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
