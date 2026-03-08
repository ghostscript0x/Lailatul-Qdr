from fpdf import FPDF
import os
import re


def strip_arabic(text):
    """Remove non-Latin characters (Arabic, emojis), keep only ASCII"""
    if not text:
        return ""
    # Keep only ASCII characters (English letters, numbers, basic punctuation)
    return re.sub(r"[^\x00-\x7F]", "", text).strip()


class RamadanPlanPDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 16)
        self.set_text_color(26, 35, 126)  # Primary color #1A237E
        self.cell(
            0,
            10,
            "Laylatul Qadr - 10 Night Worship Plan",
            border=False,
            ln=True,
            align="C",
        )
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(128)
        self.cell(
            0, 10, "Laylatul Qadr - The Night of Power | Ramadan 1447/2026", align="C"
        )


def generate_plan_pdf(nights, user_intention="", praying_for=""):
    pdf = RamadanPlanPDF()
    pdf.add_page()

    # User intention section
    if user_intention:
        pdf.set_font("helvetica", "B", 11)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 8, "Your Intention:", ln=True)
        pdf.set_font("helvetica", "", 10)
        pdf.multi_cell(0, 6, strip_arabic(user_intention))
        pdf.ln(3)

    if praying_for:
        pdf.set_font("helvetica", "B", 10)
        pdf.cell(0, 6, "Praying for:", ln=True)
        pdf.set_font("helvetica", "", 10)
        pdf.cell(0, 6, strip_arabic(praying_for), ln=True)
        pdf.ln(5)

    pdf.set_draw_color(255, 215, 0)  # Gold
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # Night cards
    for i, night in enumerate(nights):
        is_odd = night.get("is_odd", False)

        # Odd night highlight
        if is_odd:
            pdf.set_fill_color(255, 253, 231)  # Light gold/cream
            pdf.rect(10, pdf.get_y(), 190, 85, "F")

        # Night header
        pdf.set_font("helvetica", "B", 12)
        pdf.set_text_color(26, 35, 126)

        header = f"Night {night['night']} - {night['date']}"
        if is_odd:
            header += " [LIKELY LAYLATUL QADR]"
        pdf.cell(0, 8, header, ln=True)

        # Content
        pdf.set_font("helvetica", "B", 9)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(25, 6, "Recitation:", border=0)
        pdf.set_font("helvetica", "", 9)
        pdf.set_text_color(0, 0, 0)

        recitation_text = ", ".join(night.get("recitation", []))
        pdf.multi_cell(0, 6, recitation_text)

        pdf.set_font("helvetica", "B", 9)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(20, 6, "Dhikr:", border=0)
        pdf.set_font("helvetica", "", 9)
        pdf.set_text_color(0, 0, 0)
        dhikr = night.get("dhikr", {})
        dhikr_text = f"SubhanAllah {dhikr.get('subhanallah', 33)}x, Alhamdullilah {dhikr.get('alhamdullilah', 33)}x, Allahu Akbar {dhikr.get('allahu_akbar', 34)}x"
        pdf.cell(0, 6, dhikr_text, ln=True)

        pdf.set_font("helvetica", "B", 9)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(25, 6, "Tahajjud:", border=0)
        pdf.set_font("helvetica", "", 9)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 6, night.get("tahajjud", ""), ln=True)

        # Personal Dua
        pdf.set_font("helvetica", "B", 9)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(30, 6, "Personal Dua:", border=0)
        pdf.set_font("helvetica", "I", 9)
        pdf.set_text_color(0, 0, 0)
        dua_text = strip_arabic(night.get("personal_dua", ""))[:200]
        pdf.multi_cell(0, 5, dua_text)

        # Authentic Dua
        pdf.set_font("helvetica", "B", 9)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(30, 6, "Authentic Dua:", border=0)
        pdf.set_font("helvetica", "", 9)
        pdf.set_text_color(26, 35, 126)
        dua_arabic = strip_arabic(night.get(" Dua", ""))
        pdf.cell(
            0,
            6,
            dua_arabic
            if dua_arabic
            else "Allahumma innaka 'affuwwun tuhibbul-'afwa fa'fu 'anni",
            ln=True,
        )

        # Worship Tip
        pdf.set_font("helvetica", "B", 9)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(25, 6, "Tip:", border=0)
        pdf.set_font("helvetica", "", 8)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 5, strip_arabic(night.get("worship_tip", "")))

        pdf.ln(8)

        # Check for page break
        if pdf.get_y() > 220:
            pdf.add_page()

    return pdf.output(dest="S")
