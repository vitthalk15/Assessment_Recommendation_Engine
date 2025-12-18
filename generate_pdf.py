from fpdf import FPDF
import re

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'SHL Assessment Recommendation - Solution Approach', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, label):
        self.set_font('Arial', 'B', 12) # Reduced form 14
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, label, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 10) # Standard size
        self.multi_cell(0, 5, body) # Compact line height
        self.ln()

def generate_pdf(source_md, output_pdf):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    with open(source_md, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_body = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Sanitize for FPDF (Latin-1)
        line = line.replace('’', "'").replace('“', '"').replace('”', '"').replace('–', '-')
        line = line.encode('latin-1', 'replace').decode('latin-1')
            
        # Parse Headers (Assume ## is Chapter)
        if line.startswith("## "):
            if current_body:
                pdf.chapter_body(current_body)
                current_body = ""
            pdf.chapter_title(line[3:])
        elif line.startswith("# "):
            # Main Title (Skip, handled by header or first line)
            pass
        elif line.startswith("**"):
             # Metadata lines
             pdf.set_font('Arial', 'I', 10)
             pdf.cell(0, 5, line.replace('*',''), 0, 1)
             pdf.set_font('Arial', '', 10)
        else:
            current_body += line + " "

    if current_body:
        pdf.chapter_body(current_body)

    pdf.output(output_pdf)
    print(f"PDF Generated: {output_pdf}")

if __name__ == "__main__":
    generate_pdf('APPROACH.md', 'Solution_Approach.pdf')
