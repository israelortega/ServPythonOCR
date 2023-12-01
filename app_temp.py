from dotenv import load_dotenv
from flask import Flask, request, abort, jsonify, Response
import pdf_ocr_temp, json
import os
import tempfile

load_dotenv() # Carga de las variables de entorno

app = Flask(__name__)
app.config['SESSION_COOKIE_SECURE'] = False
############################################################################
@app.after_request
def set_secure_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
############################################################################
@app.route('/', methods=['GET', 'POST']) 
def hello():
    servicio =""
    try:
        servicio = "hola mundo"
    except Exception as e:
        print({e})
    return servicio
############################################################################
@app.route('/pdf', methods=['POST'])
def get():
    value = {}
    estatus_servicio = 200
    try:
        if 'archivo_pdf' not in request.files:
            raise Exception('No se ha proporcionado un archivo PDF')
        if request.files['archivo_pdf'].filename == '':
            raise Exception('No se ha cargado el archivo PDF')
        archivo_pdf = request.files['archivo_pdf']
        if archivo_pdf.filename.endswith('.pdf'):
            texto = pdf_ocr_temp.analiza_pdf_temp(archivo_pdf)
            value = {
                "resultado": texto,
                "estatus": 1,
                "mensaje": "exito"
            }
        else:
            raise Exception('El archivo proporcionado no es un PDF')
    except Exception as e:
        value = {
            "resultado": str(e),
            "estatus": 10,
            "mensaje": "error"
        }
    return Response(json.dumps(value),  status=estatus_servicio, mimetype='application/json')
############################################################################
@app.route('/err')
def generar_error():
    app.logger.debug('this is a DEBUG message')
    app.logger.info('this is an INFO message')
    app.logger.warning('this is a WARNING message')
    app.logger.error('this is an ERROR message')
    app.logger.critical('this is a CRITICAL message')
    return jsonify('hello world')
############################################################################
if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug=True)
