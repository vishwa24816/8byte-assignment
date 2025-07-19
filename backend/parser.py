import pytesseract
from PIL import Image
import re
from datetime import datetime
import magic

def parse_receipt(file_path: str) -> dict:
    """
    Parses a receipt file (image or text) and extracts structured data.
    """
    try:
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_path)

        if "text" in file_type:
            with open(file_path, "r") as f:
                text = f.read()
        else:
            text = pytesseract.image_to_string(Image.open(file_path))

        import logging
        logging.basicConfig(level=logging.INFO)
        logging.info(f"Extracted text: {text}")

        # Basic parsing logic (to be improved)
        vendor_match = re.search(r"^(.*?)\n", text)
        vendor = vendor_match.group(1).strip() if vendor_match else "Unknown"

        date_match = re.search(r"(\d{2}/\d{2}/\d{4})", text)
        transaction_date = datetime.strptime(date_match.group(1), "%m/%d/%Y").date() if date_match else None

        amount_match = re.search(r"Total\s+\$?(\d+\.\d{2})", text, re.IGNORECASE)
        amount = float(amount_match.group(1)) if amount_match else 0.0

        return {
            "vendor": vendor,
            "transaction_date": transaction_date,
            "amount": amount,
        }
    except Exception as e:
        import logging
        logging.basicConfig(level=logging.ERROR)
        logging.error(f"Error parsing receipt: {e}")
        return {}
