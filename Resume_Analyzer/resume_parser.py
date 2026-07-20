import fitz  # PyMuPDF


def extract_resume_text(pdf_path):
    """
    Extract text from a PDF resume.

    Parameters
    ----------
    pdf_path : str
        Path to the uploaded PDF file.

    Returns
    -------
    str
        Complete extracted text.
    """

    text = ""

    try:
        document = fitz.open(pdf_path)

        for page in document:
            text += page.get_text()

        document.close()

        return text.strip()

    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""
