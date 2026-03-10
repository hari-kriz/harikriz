"""
Resume Generation Engine
Reads resume_data.json and generates ATS-friendly DOCX and PDF resumes.
Strict 2-page maximum. Sections: Name, Summary, Experience, Skills, Education.
"""

import json
import sys
import os
import subprocess

try:
    from docx import Document
    from docx.shared import Pt, Inches, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-docx", "-q"])
    from docx import Document
    from docx.shared import Pt, Inches, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH


def load_data(path="resume_data.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def set_font(run, name="Calibri", size=10, bold=False, italic=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)


def add_divider(doc):
    p = doc.add_paragraph()
    p.space_before = Pt(0)
    p.space_after = Pt(3)
    pFmt = p.paragraph_format
    pFmt.space_before = Pt(0)
    pFmt.space_after = Pt(3)
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    pPr = p._element.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '4')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '2B2B5E')
    pBdr.append(bottom)
    pPr.append(pBdr)


def add_section_heading(doc, text):
    p = doc.add_paragraph()
    p.space_before = Pt(8)
    p.space_after = Pt(0)
    run = p.add_run(text.upper())
    set_font(run, size=11, bold=True, color=(43, 43, 94))
    add_divider(doc)


def generate_docx(data, output_path="Harikrishnan_2026.docx"):
    doc = Document()

    # Tight margins for 2-page fit
    for section in doc.sections:
        section.top_margin = Inches(0.4)
        section.bottom_margin = Inches(0.4)
        section.left_margin = Inches(0.55)
        section.right_margin = Inches(0.55)

    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(10)
    style.paragraph_format.space_after = Pt(0)
    style.paragraph_format.space_before = Pt(0)

    # ---- NAME ----
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.space_after = Pt(1)
    run = p.add_run(data["name"])
    set_font(run, size=18, bold=True, color=(43, 43, 94))

    # ---- TITLE ----
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.space_after = Pt(1)
    run = p.add_run(data["title"])
    set_font(run, size=10, color=(80, 80, 80))

    # ---- CONTACT ----
    contact_parts = []
    if data.get("email"):
        contact_parts.append(data["email"])
    if data.get("phone"):
        contact_parts.append(data["phone"])
    if data.get("linkedin"):
        contact_parts.append(data["linkedin"])
    if data.get("website"):
        contact_parts.append(data["website"])

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.space_after = Pt(4)
    run = p.add_run(" | ".join(contact_parts))
    set_font(run, size=8.5, color=(100, 100, 100))

    # ---- SUMMARY ----
    add_section_heading(doc, "Professional Summary")
    p = doc.add_paragraph()
    p.space_after = Pt(4)
    p.paragraph_format.space_before = Pt(3)
    run = p.add_run(data["summary"])
    set_font(run, size=9.5)

    # ---- SKILLS ----
    add_section_heading(doc, "Core Competencies")
    p = doc.add_paragraph()
    p.space_after = Pt(4)
    p.paragraph_format.space_before = Pt(3)
    run = p.add_run(" | ".join(data["skills"]))
    set_font(run, size=9.5)

    # ---- EXPERIENCE ----
    add_section_heading(doc, "Professional Experience")

    for job in data["experience"]:
        # Role + Company line
        p = doc.add_paragraph()
        p.space_before = Pt(6)
        p.space_after = Pt(0)
        role_run = p.add_run(job["role"])
        set_font(role_run, size=10.5, bold=True, color=(43, 43, 94))
        sep_run = p.add_run("  |  ")
        set_font(sep_run, size=10, color=(120, 120, 120))
        company_run = p.add_run(job["company"])
        set_font(company_run, size=10, bold=True)

        # Period + Location
        p = doc.add_paragraph()
        p.space_before = Pt(0)
        p.space_after = Pt(3)
        period_text = job["period"]
        if job.get("location"):
            period_text += "  |  " + job["location"]
        run = p.add_run(period_text)
        set_font(run, size=9, italic=True, color=(100, 100, 100))

        # Bullets
        for bullet in job["bullets"]:
            bp = doc.add_paragraph()
            bp.space_before = Pt(1)
            bp.space_after = Pt(1)
            bp.paragraph_format.left_indent = Inches(0.25)
            bp.paragraph_format.first_line_indent = Inches(-0.2)
            run = bp.add_run("\u2022  " + bullet)
            set_font(run, size=9.5)

    # ---- EDUCATION ----
    add_section_heading(doc, "Education")

    for edu in data["education"]:
        p = doc.add_paragraph()
        p.space_before = Pt(4)
        p.space_after = Pt(1)

        deg_run = p.add_run(edu["degree"])
        set_font(deg_run, size=10, bold=True)

        sep_run = p.add_run("  |  ")
        set_font(sep_run, size=9.5, color=(120, 120, 120))

        inst_run = p.add_run(edu["institution"])
        set_font(inst_run, size=9.5)

        sep_run2 = p.add_run("  |  ")
        set_font(sep_run2, size=9.5, color=(120, 120, 120))

        period_run = p.add_run(edu["period"])
        set_font(period_run, size=9.5, italic=True, color=(100, 100, 100))

        if edu.get("grade"):
            sep_run3 = p.add_run("  |  ")
            set_font(sep_run3, size=9.5, color=(120, 120, 120))
            grade_run = p.add_run(edu["grade"])
            set_font(grade_run, size=9.5, color=(80, 80, 80))

    doc.save(output_path)
    print(f"Generated: {output_path}")
    return output_path


def generate_pdf(docx_path, pdf_path="Harikrishnan_2026.pdf"):
    abs_docx = os.path.abspath(docx_path)
    abs_pdf = os.path.abspath(pdf_path)
    try:
        import win32com.client
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        doc = word.Documents.Open(abs_docx)
        doc.SaveAs(abs_pdf, FileFormat=17)
        doc.Close()
        word.Quit()
        print(f"Generated: {pdf_path}")
        return pdf_path
    except Exception as e:
        print(f"PDF generation failed: {e}")
        print("Manually convert the DOCX to PDF using Word or an online tool.")
        return None


def main():
    print("Loading resume data...")
    data = load_data()
    print("Generating DOCX...")
    docx_path = generate_docx(data)
    print("Generating PDF...")
    generate_pdf(docx_path)
    print("\nResume generation complete.")


if __name__ == "__main__":
    main()
