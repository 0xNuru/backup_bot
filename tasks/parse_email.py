#!/usr/bin/env python3

from robocorp import workitems
from RPA.PDF import PDF
from PyPDF2 import PdfReader


pdf = PDF()

def parse_email():
    """
    parse the email and extract text from the discharge letter (pdf)
    and return it as a string
    """
    item = workitems.inputs.current

    try:
        file_path = item.get_file(item.files[2])
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            print(text)
            return text
    except Exception as e:
        print(f"Error reading file: {e}")
        raise         