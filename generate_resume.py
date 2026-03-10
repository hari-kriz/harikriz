"""
Resume Generation Engine
Reads resume_data.json and generates ATS-friendly DOCX and PDF resumes.
ATS-safe: single column, no tables, no icons, no images, no decorative elements.
Natural text flow with keep-with-next to prevent orphan headings.
"""

import json
import re
import sys
import os
import subprocess

try:
    from docx import Document
    from docx.shared import Pt, Inches, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-docx", "-q"])
    from docx import Document
    from docx.shared import Pt, Inches, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_data(path="resume_data.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def sanitize(text):
    """Remove markdown, emoji, decorative chars, collapse whitespace."""
    text = re.sub(r"[*_~`#]", "", text)
    text = re.sub(r"[^\x00-\x7F]+", lambda m: m.group() if all(
        0x20 <= ord(c) <= 0x7E or c in "\n\r\t" for c in m.group()
    ) else "", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()


def set_font(run, name="Calibri", size=11, bold=False, italic=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)


def keep_with_next(paragraph):
    """Prevent heading from being separated from following content."""
    pPr = paragraph._element.get_or_add_pPr()
    kwn = OxmlElement("w:keepNext")
    pPr.append(kwn)


def keep_lines_together(paragraph):
    """Prevent paragraph from being split across pages."""
    pPr = paragraph._element.get_or_add_pPr()
    kl = OxmlElement("w:keepLines")
    pPr.append(kl)


def add_divider(doc):
    """Thin horizontal rule via bottom border on an empty paragraph."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(4)
    pPr = p._element.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "4")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "2B2B5E")
    pBdr.append(bottom)
    pPr.append(pBdr)
    keep_with_next(p)


def add_section_heading(doc, text):
    """Section heading with divider, kept with next content."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(text.upper())
    set_font(run, size=12, bold=True, color=(43, 43, 94))
    keep_with_next(p)
    add_divider(doc)


def add_bullet(doc, text, size=11, indent=0.3, spacing_before=2, spacing_after=2):
    """Add a dash-prefixed bullet paragraph."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(spacing_before)
    p.paragraph_format.space_after = Pt(spacing_after)
    p.paragraph_format.left_indent = Inches(indent)
    p.paragraph_format.first_line_indent = Inches(-0.2)
    p.paragraph_format.line_spacing = Pt(13.8)  # ~1.15 of 12pt
    run = p.add_run("- " + sanitize(text))
    set_font(run, size=size)


# ---------------------------------------------------------------------------
# Document builder
# ---------------------------------------------------------------------------

def generate_docx(data, output_path="Harikrishnan_2026.docx"):
    doc = Document()

    # ---- Page settings: A4, 1-inch margins ----
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # ---- Default style ----
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)
    style.paragraph_format.space_after = Pt(0)
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.line_spacing = Pt(13.8)

    # ==== HEADER: Name ====
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(sanitize(data["name"]))
    set_font(run, size=18, bold=True, color=(43, 43, 94))

    # ==== HEADER: Title ====
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(sanitize(data["title"]))
    set_font(run, size=12, color=(80, 80, 80))

    # ==== HEADER: Contact ====
    contact_parts = []
    for key in ("email", "phone", "linkedin", "website"):
        if data.get(key):
            contact_parts.append(data[key])
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run("  |  ".join(contact_parts))
    set_font(run, size=9, color=(100, 100, 100))

    # ==== PROFESSIONAL SUMMARY ====
    add_section_heading(doc, "Professional Summary")
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = Pt(13.8)
    run = p.add_run(sanitize(data["summary"]))
    set_font(run, size=11)

    # ==== CORE COMPETENCIES ====
    add_section_heading(doc, "Core Competencies")
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = Pt(13.8)
    skills_text = ", ".join(sanitize(s) for s in data["skills"])
    run = p.add_run(skills_text)
    set_font(run, size=11)

    # ==== PROFESSIONAL EXPERIENCE ====
    add_section_heading(doc, "Professional Experience")

    for job in data["experience"]:
        # Role line
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(0)
        keep_with_next(p)

        role_run = p.add_run(sanitize(job["role"]))
        set_font(role_run, size=11, bold=True, color=(43, 43, 94))
        sep = p.add_run("  |  ")
        set_font(sep, size=11, color=(120, 120, 120))
        co = p.add_run(sanitize(job["company"]))
        set_font(co, size=11, bold=True)

        # Period + Location
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(3)
        keep_with_next(p)
        period_text = sanitize(job["period"])
        if job.get("location"):
            period_text += "  |  " + sanitize(job["location"])
        run = p.add_run(period_text)
        set_font(run, size=10, italic=True, color=(100, 100, 100))

        # Bullets
        for bullet in job["bullets"]:
            add_bullet(doc, bullet)

    # ==== EDUCATION ====
    add_section_heading(doc, "Education")

    for edu in data["education"]:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = Pt(13.8)
        keep_lines_together(p)

        deg = p.add_run(sanitize(edu["degree"]))
        set_font(deg, size=11, bold=True)

        sep = p.add_run("  |  ")
        set_font(sep, size=11, color=(120, 120, 120))

        inst = p.add_run(sanitize(edu["institution"]))
        set_font(inst, size=11)

        sep2 = p.add_run("  |  ")
        set_font(sep2, size=11, color=(120, 120, 120))

        per = p.add_run(sanitize(edu["period"]))
        set_font(per, size=11, italic=True, color=(100, 100, 100))

        if edu.get("grade"):
            sep3 = p.add_run("  |  ")
            set_font(sep3, size=11, color=(120, 120, 120))
            gr = p.add_run(sanitize(edu["grade"]))
            set_font(gr, size=11, color=(80, 80, 80))

    doc.save(output_path)
    return output_path


# ---------------------------------------------------------------------------
# PDF conversion
# ---------------------------------------------------------------------------

def generate_pdf(docx_path, pdf_path="Harikrishnan_2026.pdf"):
    abs_docx = os.path.abspath(docx_path)
    abs_pdf = os.path.abspath(pdf_path)
    try:
        import win32com.client
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        wdoc = word.Documents.Open(abs_docx)
        wdoc.SaveAs(abs_pdf, FileFormat=17)
        wdoc.Close()
        word.Quit()
        return pdf_path
    except Exception:
        print("PDF: convert DOCX manually via Word or online tool.")
        return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    data = load_data()
    docx_path = generate_docx(data)
    generate_pdf(docx_path)
    print("Done.")


if __name__ == "__main__":
    main()
