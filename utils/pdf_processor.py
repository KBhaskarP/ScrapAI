import PyPDF2
import io

def process_pdf(pdf_file):
    """
    Extract text content from a PDF file.

    :param pdf_file: A file-like object containing the PDF data.
    :return: A string containing the extracted text from the PDF.
    """
    pdf_content = ""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    
    for page in pdf_reader.pages:
        pdf_content += page.extract_text() + "\n"
    
    return pdf_content
