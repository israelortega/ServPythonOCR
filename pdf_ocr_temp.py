import os
import fitz  # Importa la biblioteca PyMuPDF (Fitz)
import easyocr
import shutil
import tempfile
import array as arr
from array import *

def analiza_pdf_temp(archivo_pdf):
    try:
        reader = easyocr.Reader(['es'], gpu=False)  
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
            archivo_pdf.save(temp_pdf.name) 
            doc = fitz.open(temp_pdf.name)
            #Ciclo para ir de pagina en pagina
            pagina = []
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                image_list = page.get_images(full=True)
                resultText = ""
                #Ciclo para ir de imagen en imagen de cada pagina
                for img_index, img_info in enumerate(image_list):
                    xref = img_info[0]
                    base_image = doc.extract_image(xref)
                    image_data = base_image["image"]
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_image:
                        with open(temp_image.name, "wb") as image_file:
                            image_file.write(image_data)
                        # Utiliza EasyOCR para reconocer el texto en la imagen
                        result = reader.readtext(temp_image.name)
                    for detection in result:
                        text = detection[1]
                        resultText = resultText + " " + text
                pagina.append(resultText)
    except Exception as e:
        raise Exception(str(e))
    return pagina