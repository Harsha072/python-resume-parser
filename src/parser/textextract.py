import pdfplumber
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

# Provide the PDF file path here
pdf_file_path = r"E:\fulltime\spl\youcanbookme\Puttaswamy_Harsha_CV.pdf"

extracted_text = extract_text_from_pdf(pdf_file_path)
print("Extracted Text:\n", extracted_text)
