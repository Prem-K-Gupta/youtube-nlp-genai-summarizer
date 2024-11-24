from fpdf import FPDF
from io import BytesIO
import os

def generate_pdf(summary, concepts, sentiment_label, sentiment_score, sentiment_explanation, topics, insights):
    """
    Generate a PDF document containing video summary, sentiment analysis, topics, key concepts, and contextual insights.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", style="", fname="DejaVuSans.ttf")  
    pdf.set_font("DejaVu", size=12)

    # Add the header
    pdf.cell(200, 10, text="Video Summary and Notes", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(10)

    # Add Summary
    pdf.multi_cell(0, 10, text=f"Summary:\n{summary}", border=0)
    pdf.ln(5)

    # Add Sentiment Analysis
    pdf.multi_cell(0, 10, text=f"Sentiment:\n{sentiment_label} ({sentiment_score:.2f})\nExplanation: {sentiment_explanation}", border=0)
    pdf.ln(5)

    # Add Topics
    pdf.multi_cell(0, 10, text=f"Topics:\n{', '.join(topics)}", border=0)
    pdf.ln(5)

    # Add Key Concepts
    pdf.multi_cell(0, 10, text=f"Key Concepts:\n{', '.join(concepts)}", border=0)
    pdf.ln(5)

    # Add Contextual Insights
    pdf.cell(200, 10, text="Contextual Insights:", new_x="LMARGIN", new_y="NEXT")
    for concept, info in insights.items():
        pdf.multi_cell(0, 10, text=f"{concept}: {info}", border=0)
        pdf.ln(2)

    # Save the PDF to memory
    pdf_memory = BytesIO()
    pdf.output(pdf_memory)
    pdf_memory.seek(0)
    return pdf_memory


def generate_and_save_pdf(summary, concepts, sentiment_label, sentiment_score, sentiment_explanation, topics, insights, filename):
    """
    Generate a PDF file and save it to a specific directory.
    """
    # Generate the PDF in memory
    pdf_data = generate_pdf(
        summary, concepts, sentiment_label, sentiment_score, sentiment_explanation, topics, insights
    )

    # Ensure the directory for saving PDFs exists
    save_dir = "saved_pdfs"
    os.makedirs(save_dir, exist_ok=True)

    # Save the PDF to a file
    pdf_path = os.path.join(save_dir, filename)
    with open(pdf_path, "wb") as f:
        f.write(pdf_data.getvalue())

    return pdf_path
