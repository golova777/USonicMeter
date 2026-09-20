# утилита для создания *.py файла содержащего base64 строку представляющую
# файл шаблона отчёт - с диагнозом
# Ожидается, что в текущей директории находится файл "template.docx"
# На выходе утилита создаст новый файл "template_docx.py"
# в котором будет содержаться переменная [TEMPLATE_DOCX: str] с base64-кодированным
# содержимым файла "template.docx"


import base64

EXPECTED_TEMPLATE_FILE = "template.docx"
SAVE_FILE_PY = "template_docx.py"
TEMPLATE_HOLDER_VARIABLE = "TEMPLATE_BASE64_STRING"







if __name__ == "__main__":
    try:
        with open(EXPECTED_TEMPLATE_FILE, "rb") as file:
            binary_data = file.read()
            data_b64 = base64.b64encode(binary_data).decode()

            with open(SAVE_FILE_PY, "+w", encoding="utf-8") as txt_file:
                data = f"{TEMPLATE_HOLDER_VARIABLE} = '{data_b64}'"
                txt_file.write(data)


    except Exception as e:
        print("ошибка работы с файлом шаблона: ", e)











