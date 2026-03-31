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


def load_data(path="resume_data.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def sanitize(text):
    text = re.sub(r"[*_~`#]", "", text)
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
    pPr = paragraph._element.get_or_add_pPr()
    pPr.append(OxmlElement("w:keepNext"))


def keep_lines(paragraph):
    pPr = paragraph._element.get_or_add_pPr()
    pPr.append(OxmlElement("w:keepLines"))


def add_divider(doc):
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
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(text.upper())
    set_font(run, size=12, bold=True, color=(43, 43, 94))
    keep_with_next(p)
    add_divider(doc)


def add_bullet(doc, text, size=11, indent=0.3):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1.5)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.left_indent = Inches(indent)
    p.paragraph_format.first_line_indent = Inches(-0.2)
    p.paragraph_format.line_spacing = Pt(13.8)
    run = p.add_run("- " + sanitize(text))
    set_font(run, size=size)


def generate_docx(data, output_path="Harikrishnan_2026.docx"):
    doc = Document()

    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)

    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)
    style.paragraph_format.space_after = Pt(0)
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.line_spacing = Pt(13.8)

    # NAME
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(sanitize(data["name"]))
    set_font(run, size=18, bold=True, color=(43, 43, 94))

    # CONTACT
    contact_parts = []
    for key in ("phone", "email", "linkedin"):
        if data.get(key):
            contact_parts.append(data[key])
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run("  |  ".join(contact_parts))
    set_font(run, size=9, color=(100, 100, 100))

    # SUMMARY
    add_section_heading(doc, "Professional Summary")
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = Pt(13.8)
    run = p.add_run(sanitize(data["summary"]))
    set_font(run, size=11)

    # SKILLS
    add_section_heading(doc, "Skills")
    for skill_line in data["skills"]:
        add_bullet(doc, skill_line, size=10.5)

    # EXPERIENCE
    add_section_heading(doc, "Work Experience")

    for job in data["experience"]:
        # Company + Location
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(0)
        keep_with_next(p)
        co = p.add_run(sanitize(job["company"]))
        set_font(co, size=11, bold=True)
        if job.get("location"):
            loc = p.add_run("  -  " + sanitize(job["location"]))
            set_font(loc, size=10, italic=True, color=(100, 100, 100))

        # Role + Period
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(3)
        keep_with_next(p)
        role = p.add_run(sanitize(job["role"]))
        set_font(role, size=11, bold=True, color=(43, 43, 94))
        sep = p.add_run("  |  ")
        set_font(sep, size=10, color=(150, 150, 150))
        per = p.add_run(sanitize(job["period"]))
        set_font(per, size=10, italic=True, color=(100, 100, 100))

        # Categories (for first job) or flat bullets
        if job.get("categories"):
            for cat in job["categories"]:
                cp = doc.add_paragraph()
                cp.paragraph_format.space_before = Pt(5)
                cp.paragraph_format.space_after = Pt(2)
                keep_with_next(cp)
                cr = cp.add_run(sanitize(cat["name"]))
                set_font(cr, size=10.5, bold=True, italic=True, color=(68, 68, 68))
                for bullet in cat["bullets"]:
                    add_bullet(doc, bullet, size=10.5)
        elif job.get("bullets"):
            for bullet in job["bullets"]:
                add_bullet(doc, bullet, size=10.5)

    # PROJECTS
    if data.get("projects"):
        add_section_heading(doc, "Key Projects")
        for i, proj in enumerate(data["projects"], 1):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(2)
            keep_with_next(p)
            run = p.add_run(f"{i}. {sanitize(proj['title'])}")
            set_font(run, size=11, bold=True)

            for label_key in ("problem", "action", "impact"):
                if proj.get(label_key):
                    bp = doc.add_paragraph()
                    bp.paragraph_format.space_before = Pt(1)
                    bp.paragraph_format.space_after = Pt(1)
                    bp.paragraph_format.left_indent = Inches(0.2)
                    bp.paragraph_format.line_spacing = Pt(13.8)
                    lbl = bp.add_run(label_key.capitalize() + ": ")
                    set_font(lbl, size=10.5, bold=True, color=(43, 43, 94))
                    txt = bp.add_run(sanitize(proj[label_key]))
                    set_font(txt, size=10.5)

    # EDUCATION
    add_section_heading(doc, "Education")
    for edu in data["education"]:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(5)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = Pt(13.8)
        keep_lines(p)

        deg = p.add_run(sanitize(edu["degree"]))
        set_font(deg, size=11, bold=True)
        sep = p.add_run(" - ")
        set_font(sep, size=11, color=(120, 120, 120))
        inst = p.add_run(sanitize(edu["institution"]))
        set_font(inst, size=11)
        if edu.get("grade"):
            gr = p.add_run(" (" + sanitize(edu["grade"]) + ")")
            set_font(gr, size=10, color=(80, 80, 80))
        sep2 = p.add_run("  |  ")
        set_font(sep2, size=10, color=(120, 120, 120))
        per = p.add_run(sanitize(edu["period"]))
        set_font(per, size=10, italic=True, color=(100, 100, 100))

    doc.save(output_path)
    return output_path


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


def main():
    data = load_data()
    docx_path = generate_docx(data)
    generate_pdf(docx_path)
    print("Done.")


if __name__ == "__main__":
    main()
