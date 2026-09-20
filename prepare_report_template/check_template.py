from template_docx import TEMPLATE_BASE64_STRING
import base64
import io

with open("test.docx", "wb") as file:
    bin_data = io.BytesIO(base64.b64decode(TEMPLATE_BASE64_STRING)).read()
    file.write(bin_data)