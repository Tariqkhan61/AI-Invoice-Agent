#python
import os
from datetime import datetime

from dotenv import load_dotenv
from google import genai

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib.enums import TA_CENTER, TA_RIGHT


# ==============================
# LOAD API KEY
# ==============================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ GEMINI_API_KEY nahi mili!")
    exit()

client = genai.Client(api_key=api_key)


# ==============================
# CREATE PROFESSIONAL PDF
# ==============================

def create_pdf(customer, item, quantity, price, total):

    invoice_number = "INV-" + datetime.now().strftime("%Y%m%d%H%M%S")
    invoice_date = datetime.now().strftime("%d %B %Y")

    filename = "invoice.pdf"

    document = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()

    story = []

    # ==============================
    # HEADER
    # ==============================

    title_style = styles["Title"]
    title_style.fontName = "Helvetica-Bold"
    title_style.fontSize = 24
    title_style.alignment = TA_CENTER
    title_style.textColor = colors.HexColor("#173F5F")

    story.append(Paragraph("AI INVOICE", title_style))
    story.append(Spacer(1, 8))

    subtitle_style = styles["Normal"]
    subtitle_style.alignment = TA_CENTER
    subtitle_style.fontSize = 10
    subtitle_style.textColor = colors.grey

    story.append(Paragraph(
        "Professional Invoice Generator",
        subtitle_style
    ))

    story.append(Spacer(1, 20))

    # ==============================
    # INVOICE INFORMATION
    # ==============================

    info_data = [
        [
            Paragraph("<b>Invoice Number</b>", styles["Normal"]),
            invoice_number,
            Paragraph("<b>Date</b>", styles["Normal"]),
            invoice_date,
        ],
        [
            Paragraph("<b>Billed To</b>", styles["Normal"]),
            customer,
            "",
            "",
        ],
    ]

    info_table = Table(
        info_data,
        colWidths=[35 * mm, 65 * mm, 25 * mm, 45 * mm]
    )

    info_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EAF2F8")),
            ("BACKGROUND", (2, 0), (2, 0), colors.HexColor("#EAF2F8")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("SPAN", (1, 1), (3, 1)),
        ])
    )

    story.append(info_table)
    story.append(Spacer(1, 25))

    # ==============================
    # ORDER DETAILS
    # ==============================

    story.append(
        Paragraph("<b>Order Details</b>", styles["Heading2"])
    )

    story.append(Spacer(1, 8))

    table_data = [
        [
            Paragraph("<b>Description</b>", styles["Normal"]),
            Paragraph("<b>Quantity</b>", styles["Normal"]),
            Paragraph("<b>Unit Price</b>", styles["Normal"]),
            Paragraph("<b>Total</b>", styles["Normal"]),
        ],
        [
            item,
            str(quantity),
            f"PKR {price:,.2f}",
            f"PKR {total:,.2f}",
        ],
    ]

    order_table = Table(
        table_data,
        colWidths=[75 * mm, 25 * mm, 40 * mm, 40 * mm]
    )

    order_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#173F5F")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.7, colors.lightgrey),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("ALIGN", (2, 1), (-1, 1), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (-1, 1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ])
    )

    story.append(order_table)
    story.append(Spacer(1, 20))

    # ==============================
    # TOTALS
    # ==============================

    totals_data = [
        ["Subtotal:", f"PKR {total:,.2f}"],
        ["Tax / Discount:", "PKR 0.00"],
        ["TOTAL AMOUNT DUE:", f"PKR {total:,.2f}"],
    ]

    totals_table = Table(
        totals_data,
        colWidths=[110 * mm, 50 * mm],
        hAlign="RIGHT"
    )

    totals_table.setStyle(
        TableStyle([
            ("ALIGN", (1, 0), (1, -1), "RIGHT"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),

            ("LINEABOVE", (0, 2), (-1, 2), 1.2, colors.HexColor("#173F5F")),

            ("FONTNAME", (0, 2), (-1, 2), "Helvetica-Bold"),
            ("FONTSIZE", (0, 2), (-1, 2), 13),
            ("TEXTCOLOR", (0, 2), (-1, 2), colors.HexColor("#173F5F")),
        ])
    )

    story.append(totals_table)
    story.append(Spacer(1, 35))

    # ==============================
    # THANK YOU
    # ==============================

    thank_you_style = styles["Normal"]
    thank_you_style.alignment = TA_CENTER
    thank_you_style.fontSize = 10
    thank_you_style.textColor = colors.grey

    story.append(
        Paragraph(
            "<b>Thank you for your business!</b>",
            thank_you_style
        )
    )

    story.append(Spacer(1, 5))

    story.append(
        Paragraph(
            "Generated by AI Invoice Agent",
            thank_you_style
        )
    )

    # Build PDF
    document.build(story)

    print(f"\n📄 Professional PDF created: {filename}")
    print(f"🧾 Invoice Number: {invoice_number}")


# ==============================
# INVOICE AGENT
# ==============================

def invoice_agent():

    print("🤖 AI Invoice Agent")
    print("-------------------")

    customer = input("Customer ka naam: ")
    item = input("Service/Product ka naam: ")
    quantity = int(input("Quantity: "))
    price = float(input("Per item price (PKR): "))

    total = quantity * price

    # Console invoice
    print("\n========== INVOICE ==========")
    print(f"Customer : {customer}")
    print(f"Item     : {item}")
    print(f"Quantity : {quantity}")
    print(f"Price    : PKR {price:,.2f}")
    print("-----------------------------")
    print(f"TOTAL    : PKR {total:,.2f}")
    print("=============================")

    # Create professional PDF
    create_pdf(
        customer,
        item,
        quantity,
        price,
        total
    )

    # ==============================
    # GEMINI AI SUMMARY
    # ==============================

    prompt = f"""
    Create a short professional invoice summary.

    Customer: {customer}
    Product/Service: {item}
    Quantity: {quantity}
    Price per item: PKR {price:,.2f}
    Total: PKR {total:,.2f}

    Keep it professional and concise.
    """

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    print("\n🤖 AI SUMMARY")
    print("-------------------")
    print(response.text)


# Start the agent
invoice_agent()

